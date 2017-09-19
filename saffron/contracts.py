import re
import os
import json
import pprint
import random
import logging
import argparse
import subprocess
from io import BytesIO

import web3
from web3 import Web3, HTTPProvider
from web3.eth import Eth, Contract
from solc import compile_source, compile_standard
from jinja2 import Environment
from jinja2.nodes import Name

from saffron.accounts import Account
from saffron.genesis import Chain
from saffron import database
import sqlite3

import pickle
import getpass

log = logging.getLogger(__file__)

DEFAULT_CONTRACT_DIRECTORY = './contracts'

def update_contract(address, instance, name):
	return database.update_contract(address, instance, name)

def get_template_variables(fo):
	nodes = Environment().parse(fo.read()).body[0].nodes
	var_names = [x.name for x in nodes if type(x) is Name]
	return var_names

def render_contract(payload, contract_directory=DEFAULT_CONTRACT_DIRECTORY):
	sol_contract = payload.pop('sol')
	template_variables = get_template_variables(BytesIO(sol_contract.encode()))
	assert 'contract_name' in payload
	name = payload.get('contract_name')
	assert all(x in template_variables for x in list(payload.keys()))
	template = Environment().from_string(sol_contract)
	return name, template.render(payload)

def load_tsol_file(file=None, payload=None):
	assert file and payload, 'No file or payload provided.'
	payload['sol'] = file.read()
	name, rendered_contract = render_contract(payload=payload)
	return name, rendered_contract

def name_is_unique(name):
	_name, _address = database.contract_exists(name=name)
	if _name is None and _address is None:
		return True
	return False

def load_sol_file(file=None):
	assert file, 'No file provided'
	return file.read()


class Contract(Contract):
	def __init__(self, name, sol_file_path):
		assert name != None, 'A name identifier must be provided to create a new contract instance.'
		_name, _address = database.contract_exists(name=name)
		assert _name is None and _address is None
		node_info = json.loads(open(os.environ['NODE_INFO_JSON']).read())
		self.web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:{port}".format(port=node_info.get('rpcport'))))
		self.name = name
		self.is_deployed = None
		with open(sol_file_path) as f:
			self.sol = load_sol_file(f)
		self.template_json = Environment().from_string(database.input_json).render(name=self.name, sol=json.dumps(self.sol))
		self.output_json = compile_standard(json.loads(self.template_json))
		self.compiled_name = list(self.output_json['contracts'][self.name].keys())[0]
		self.contracts = self.output_json['contracts'][self.name][self.compiled_name]
		self.abi = self.contracts['abi']
		self.metadata = self.contracts['metadata']
		self.bytecode = self.contracts['evm']['deployedBytecode']['object']
		self.gas_estimates = self.contracts['evm']['gasEstimates']
		self.method_identifiers = self.contracts['evm']['methodIdentifiers']

		# set in deploy
		self.address = None
		self.instance = None
		self.defaulAccount = None

	def __str__(self):
		return 'Contract {}, {}'.format(self.address if self.address else 'None', self.name if self.name else 'None')

	def from_chain(self):
		raise NotImplementedError('TODO')

	def deploy(self, cwd=False):
		assert not self.is_deployed, 'This contract already exists on the chain.'
		assert self.sol, 'No solidity code loaded into this object'
		response = database.insert_contract(self.name,
											self.abi,
											self.bytecode,
											self.gas_estimates,
											self.method_identifiers,
											cwd)
		okay = web3.personal.Personal(self.web3)
		options = 'Unlock: \n' + '\n'.join([' '.join([str(i),':',x]) for i, x in enumerate(okay.listAccounts)]) + '\n'
		self.defaultAccount = okay.listAccounts[int(input(options))]
		result = okay.unlockAccount(self.defaultAccount, getpass.getpass('\nPassword:'), 5000)
		if result:
			self.address = self.web3.eth.sendTransaction(transaction={'data' : '0x' + self.bytecode, 'from': self.defaultAccount, 'gaslimit': 30000})
			self.instance = self.web3.eth.contract(self.address)
		else:
			raise Exepction('unable to unlock account')
		#update the deployed and address to the db and an instance for pulling and interacting with the contract again
		return update_contract(json.dumps(self.address), self.method_identifiers, self.name)


