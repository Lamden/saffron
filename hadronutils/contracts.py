import re
import os
import json
import pprint
import random
import argparse
import subprocess
from io import StringIO
from genesis import Chain

import web3
from web3.eth import Eth
from solc import compile_source, compile_standard

from jinja2 import Environment
from jinja2.nodes import Name

import accounts
import utils

DEFAULT_CONTRACT_DIRECTORY = './contracts'

class Contract():
	def __init__(self):
		self.chain = Chain()

	def __str__(self):
		return 'Contract {}, {}'.format(self.address if self.address else 'None', self.name if self.name else 'None')

	def from_db(self, name=None, address=None):
		assert self.chain, 'No chain provided.'
		self = Contract.from_db(name=name, address=address)

	def from_chain(self):
		pass

	def load_sol_file(self, file=None):
		assert self.chain, 'No chain provided.'
		assert file, 'No file provided'

		self.sol = file.read()

	def load_tsol_file(self, file=None, payload=None):
		assert self.chain, 'No chain provided.'
		assert file and payload, 'No file or payload provided.'

		payload['sol'] = file.read()

		self.sol = Accounts.generate_new_contract(payload=payload)

	def deploy(self):
		assert not self.is_deployed, 'This contract already exists on the chain.'
		assert self.sol, 'No solidity code loaded into this object'

		#compile sol
		input_json = {
			'language': 'Solidity',
			'sources': {
				self.name: {
					'content': self.sol
				}
			},
			'settings': {
				'outputSelection': {
					'*': {
						'*': [ 'metadata', 'evm.bytecode', 'abi', 'evm.bytecode.opcodes', 'evm.gasEstimates', 'evm.methodIdentifiers' ]
					}
				}
			}
		}

		output_json = compile_standard(input_json)

		compiled_name = list(output_json['contracts'][self.name].keys())[0]

		#break output into bits to store into the db for simple access
		self.abi = output_json['contracts'][self.name][compiled_name]['abi']
		self.metadata = output_json['contracts'][self.name][compiled_name]['metadata']
		self.bytecode = output_json['contracts'][self.name][compiled_name]['evm']['deployedBytecode']['object']
		self.gas_estimate = output_json['contracts'][self.name][compiled_name]['evm']['gasEstimates']
		self.method_identifiers = output_json['contracts'][self.name][compiled_name]['evm']['methodIdentifiers']

		#pickle the blobs and add them to the db

		#deploy to the blockchain

		#update the deployed and address to the db

	@classmethod
	def new(self, name):
		assert name != None, 'A name identifier must be provided to create a new contract instance.'
		assert name_is_unique(name), 'A unique identifier must be provided.'
		c = Contract()
		c.name = name
		return c

	@classmethod
	def name_is_unique(self, name):
		return True if Contract().from_db(name) != None else False

	@classmethod
	def get_template_variables(self, fo):
		nodes = Environment().parse(fo.read()).body[0].nodes
		var_names = [x.name for x in nodes if type(x) is Name]
		return var_names

	@classmethod
	def from_db(self, name=None, address=None):
		c = Chain().database.select_contract(name=name, address=address)
		if c.is_deployed:
			try:
				c.instance = Eth.contract(name=c.name, address=c.address)
			except:
				c = None
		return c

	@classmethod
	def generate_new_contract(self, payload, contract_directory=DEFAULT_CONTRACT_DIRECTORY):
		sol_contract = payload.pop('sol')
		template_variables = self.get_template_variables(StringIO(sol_contract))
		assert 'contract_name' in payload
		self.name = payload.get('contract_name')
		assert all(x in template_variables for x in list(payload.keys()))
		template = Environment().from_string(sol_contract)
		return template.render(payload)