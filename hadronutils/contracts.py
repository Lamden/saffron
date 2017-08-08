import re
import os
import json
import pprint
import random
import argparse
import subprocess
from io import StringIO

import web3
from web3.eth import Eth
from solc import compile_source, compile_standard

from jinja2 import Environment
from jinja2.nodes import Name

from hadronutils.accounts import Account
from hadronutils.utils import *
from hadronutils.genesis import Chain

DEFAULT_CONTRACT_DIRECTORY = './contracts'

save_contract_sql = '''
			INSERT INTO contracts VALUES (
			name {}, 
			abi {},
			metadata {},
			gas_estimates {},
			method_identifiers {}
			)'''.format

update_contracts_sql = '''
			UPDATE contracts 
			SET 
			address = {}, 
			instance = {}, 
			is_deployed = true 
			WHERE 
			name = {}'''.format

input_json = '''{
			'language': 'Solidity',
			'sources': {
				{name}: {
					'content': {sol}
				}
			},
			'settings': {
				'outputSelection': {
					'*': {
						'*': [ 'metadata', 'evm.bytecode', 'abi', 'evm.bytecode.opcodes', 'evm.gasEstimates', 'evm.methodIdentifiers' ]
					}
				}
			}
		}'''.format

def insert_contract(name, abi, bytecode, gas_estimates, method_identifiers):
	#pickle the blobs and add them to the db
	s = insert_contract_sql(name,
					abi,
					bytecode,
					pickle.dumps(gas_estimates),
					pickle.dumps(method_identifiers))
	return Chain().database.cursor.execute(s)

def update_contract(address, instance, name):
	Chain().database.cursor.execute(update_contracts_sql(address, instance, name))

chain = Chain()

def get_template_variables(fo):
	nodes = Environment().parse(fo.read()).body[0].nodes
	var_names = [x.name for x in nodes if type(x) is Name]
	return var_names

def render_contract(payload, contract_directory=DEFAULT_CONTRACT_DIRECTORY):
	sol_contract = payload.pop('sol')
	template_variables = get_template_variables(StringIO(sol_contract))
	assert 'contract_name' in payload
	name = payload.get('contract_name')
	assert all(x in template_variables for x in list(payload.keys()))
	template = Environment().from_string(sol_contract)
	return name, template.render(payload)

def load_tsol_file(file=None, payload=None):
	assert chain, 'No chain provided.'
	assert file and payload, 'No file or payload provided.'
	payload['sol'] = file.read()
	name, rendered_contract = render_contract(payload=payload)
	return name, rendered_contract

def name_is_unique(name):
	return True if Contract().from_db(name) != None else False

def load_sol_file(file=None):
	assert chain, 'No chain provided.'
	assert file, 'No file provided'
	return file.read()

def from_db(self, name=None, address=None):
	c = Chain().database.select_contract(name=name, address=address)
	if c.is_deployed:
		try:
			c.instance = Eth.contract(address=c.address)
		except:
			c = None
	return c


class Contract():
	def __init__(self, name, sol_file_path):
		assert name != None, 'A name identifier must be provided to create a new contract instance.'
		assert name_is_unique(name), 'A unique identifier must be provided.'
		self.name = name
		self.is_deployed = None
		self.sol = load_sol_file(sol_file_path)
		self.output_json = compile_standard(json.loads(input_json.format(name=self.name, sol=self.sol)))
		self.compiled_name = list(output_json['contracts'][self.name].keys())[0]
		self.contracts = output_json['contracts'][self.name][compiled_name]
		self.abi = self.contracts['abi']
		self.metadata = self.contracts['metadata']
		self.bytecode = self.contracts['evm']['deployedBytecode']['object']
		self.gas_estimate = self.contracts['evm']['gasEstimates']
		self.method_identifiers = self.contracts['evm']['methodIdentifiers']
		
		# set in deploy
		self.address = None
		self.instance = None

	def __str__(self):
		return 'Contract {}, {}'.format(self.address if self.address else 'None', self.name if self.name else 'None')

	def from_chain(self):
		raise NotImplementedError('TODO')

	def deploy(self):
		assert not self.is_deployed, 'This contract already exists on the chain.'
		assert self.sol, 'No solidity code loaded into this object'

		response = save_contract(self.name,
								self.abi,
								self.bytecode,
								self.gas_estimates,
								self.method_identifiers)
		# deploy contract
		self.address = Eth.sendTransaction({'data' : self.bytecode})
		self.instance = Eth.contract(self.address)
		#update the deployed and address to the db and an instance for pulling and interacting with the contract again
		update_contract(self.address, self.instance, self.name)


