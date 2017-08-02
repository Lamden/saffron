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
from jinja2 import Environment
from jinja2.nodes import Name

import accounts
import utils

DEFAULT_CONTRACT_DIRECTORY = './contracts'

class Contract():
	chain = None
	name = None
	is_deployed = None
	address = None
	instance = None

	def __init__(self):
		self.chain = Chain()

	def __str__(self):
		return 'Contract {}, {}'.format(self.address if self.address else 'None', self.name if self.name else 'None')

	def from_db(self, name=None, address=None):
		assert self.chain, "No chain provided."
		self = Contract.from_db(name=name, address=address)

	# def deploy(self):
	# 	assert self.chain, "No chain provided."
	# 	if not self.is_deployed:
	# 		self.instance.deploy(self.address)
	# 	pass

	def load_sol_file(self, filename=None):
		assert self.chain, "No chain provided."
		pass

	def load_tsol_file(self, filename=None, payload=None):
		assert self.chain, "No chain provided."
		pass

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
				pass
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