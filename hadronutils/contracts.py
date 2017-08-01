import re
import os
import json
import pprint
import random
import argparse
import subprocess
from io import StringIO

from jinja2 import Environment
from jinja2.nodes import Name

import accounts
import utils

DEFAULT_CONTRACT_DIRECTORY = './contracts'

class Contract:
	def __init__(self, name=None, deployed=False, address=None):	
		self.name = name
		self.deployed = deployed
		self.address = address
		self.contract_name = None
		self.abi = None
		self.payload = None

	@classmethod
	def get_template_variables(self, fo):
		nodes = Environment().parse(fo.read()).body[0].nodes
		var_names = [x.name for x in nodes if type(x) is Name]
		return var_names

	@classmethod
	def generate_new_contract(self, payload, contract_directory=DEFAULT_CONTRACT_DIRECTORY):
		sol_contract = payload.pop('sol')
		template_variables = self.get_template_variables(StringIO(sol_contract))
		assert 'contract_name' in payload
		self.name = payload.get('contract_name')
		assert all(x in template_variables for x in list(payload.keys()))
		template = Environment().from_string(sol_contract)
		return template.render(payload)

