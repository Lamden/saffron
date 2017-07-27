import subprocess
import argparse
import random
import pprint
import json
import os
import accounts
import utils

def create_genesis_block(genesisBlockPayload):
	assert all(x in \
	['config',
	'alloc',
	'coinbase',
	'difficulty',
	'extraData',
	'gasLimit',
	'nonce',
	'mixhash',
	'parentHash',
	'timestamp'] \
	for x in list(genesisBlockPayload.keys()))
	
	assert all(x in \
	['chainId',
	'homesteadBlock',
	'eip155Block',
	'eip158Block'] \
	for x in list(genesisBlockPayload['config'].keys()))

	with open('genesis.json', 'w') as fp:
		json.dump(genesisBlockPayload, fp)

def initialize_chain(datadirPath, genesisBlockPath):
	subprocess.run('geth --datadir ' + datadirPath + ' init ' + genesisBlockPath)

def run_generator():
	if not utils.check_if_in_project():
		# create a new chain!
		print('=== Project Name ===')
		projectDir = input('Name your new Hadron project: ')

		while True:
			print('\n=== Blockchain Settings ===')
			genesis = utils.GENESIS_BLOCK_TEMPLATE

			# data formatting
			user_input = input('Chain ID: ')
			genesis['config']['chainId'] = utils.formatting(user_input)
			print('Chain ID set to {}'.format(genesis['config']['chainId']))

			user_input = input('Difficulty: ')
			user_input = utils.formatting(user_input)

			if user_input > utils.INT16:
				user_input = utils.INT16

			genesis['difficulty'] = hex(user_input)
			print('Difficulty set to {}'.format(genesis['difficulty']))

			user_input = input('Gas Limit: ')
			user_input = utils.formatting(user_input)

			if user_input > utils.INT16:
				user_input = utils.INT16

			genesis['gasLimit'] = hex(user_input)
			print('Gas Limit set to {}'.format(genesis['gasLimit']))

			print('\n=== Hashing Variables ===')
			genesis['nonce'] = utils.generate_hex_string(16)
			print('Random nonce generated as {}'.format(genesis['nonce']))

			genesis['mixhash'] = utils.generate_hex_string(64)
			print('Random mix hash generated as {}'.format(genesis['mixhash']))

			genesis['parentHash'] = utils.generate_hex_string(64)
			print('Random parent hash generated as {}'.format(genesis['parentHash']))
			
			print('\n=== Generating Genesis Block ===')
			print('Does the following payload look correct?\n')
			pprint.pprint(genesis)
			user_input = input('\n(y/n): ')
			if user_input is 'y':
				break
			print('\n... Throwing away old data and starting fresh ...\n')

		os.makedirs(projectDir, exist_ok=True)
		PROJECT_DIR = projectDir
		os.chdir(projectDir)
		print('Directory created in: {}'.format(os.getcwd()))

		create_genesis_block(genesis)
		print('Genesis block written!')

		print('\n=== Initializing Chain... ===\n')
		initialize_chain('.', 'genesis.json')
		print('\nChain initialized!')

		user_input = input('Enter password for default account: ')
		accounts.create_account(user_input)
	else:
		print('Already in a project directory...')

run_generator()