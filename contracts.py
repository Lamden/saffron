import subprocess
import argparse
import random
import pprint
import json
import os
import accounts
import utils
import re
import pprint

SEAGULL_OPEN = '{{'
SEAGULL_CLOSE = '}}'

DEFAULT_CONTRACT_DIRECTORY = './contracts'

def get_template_variables(filename):
	file_string = None
	with open(filename, 'r') as f:
		file_string = f.read()

	variable_definition_starting_point = [m.start() for m in re.finditer(SEAGULL_OPEN, file_string)]
	variable_definition_ending_point = [m.end() for m in re.finditer(SEAGULL_CLOSE, file_string)]

	template_variable_indexes = list(zip(variable_definition_starting_point, variable_definition_ending_point))

	variables = []
	for var in template_variable_indexes:
		variables.append(file_string[var[0]:var[1]].strip(SEAGULL_OPEN + SEAGULL_CLOSE))

	return variables

def generate_new_contract(template_file_name, payload, name, contract_directory=DEFAULT_CONTRACT_DIRECTORY):
	template_variables = get_template_variables(template_file_name)
	assert all(x in template_variables for x in list(payload.keys()))
	assert name != None

	file_string = None
	with open(template_file_name, 'r') as f:
		file_string = f.read()

	for key in template_variables:
		file_string = file_string.replace(SEAGULL_OPEN + key + SEAGULL_CLOSE, payload[key])

	with open('{}/{}.sol'.format(contract_directory, name), 'w') as f:
		f.write(file_string)

# print(generate_default_contract_code('Autoria'))
# create_new_contract('Autoria')

pprint.pprint(get_template_variables('C:/Users/stuart/Desktop/hadron_chain_example/hadron/contract_templates/fixed_supply_token.tsol'))

payload = {'asset_name': 'DICK',
'contract_name': 'Something',
'solidity_version': '0.4.11',
'symbol': 'DIQ',
'total_supply': '100000000000000000000000'}

pprint.pprint(generate_new_contract('C:/Users/stuart/Desktop/hadron_chain_example/hadron/contract_templates/fixed_supply_token.tsol', payload, 'Testing'))