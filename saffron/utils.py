import random
import pprint
import json
import subprocess
import os
import time
from threading import Thread
import re
from saffron import settings
#from saffron.genesis import Chain
import getpass
import configparser
from os.path import join

GENESIS_BLOCK_TEMPLATE = {
	'config': {
	    'chainId': 0,
	    'homesteadBlock': 0,
	    'eip155Block': 0,
	    'eip158Block': 0
		},
	'alloc'      : {},
	'coinbase'   : '0x0000000000000000000000000000000000000000',
	'difficulty' : '0x0',
	'extraData'  : '',
	'gasLimit'   : '0x0',
	'nonce'      : '0x0000000000000000',
	'mixhash'    : '0x0000000000000000000000000000000000000000000000000000000000000000',
	'parentHash' : '0x0000000000000000000000000000000000000000000000000000000000000000',
	'timestamp'  : '0x00'
}

INT16 = 18446744073709551615

def check_if_in_project():
	try:
		f = open('config.lamden', 'r')
		return True
	except:
		return False

def formatting(i):
	try:
		i = int(i)
	except:
		i = 0

	if i < 0:
		i = 0
	return i

def generate_hex_string(length):
	string = '0x'
	for i in range(length):
		string += hex(random.randint(0, 16))[-1]
	return string

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

	with open(os.path.join(settings.lamden_folder_path, 'genesis.json'), 'w') as fp:
		json.dump(genesisBlockPayload, fp)

def initialize_chain(project_dir, genesisBlockFp):
	#Chain(project_dir=settings.lamden_folder_path, genesis_block_path=os.path.join(settings.lamden_folder_path, genesisBlockFp))
	subprocess.Popen(['nohup', 'geth --datadir ' + settings.lamden_folder_path + ' init ' + os.path.join(settings.lamden_folder_path, genesisBlockFp)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def run_generator():
	if not check_if_in_project():
		# create a new chain!
		print('=== Project Name ===')
		project_dir = input('Name your new Lamden project: ')

		while True:
			print('\n=== Blockchain Settings ===')
			genesis = GENESIS_BLOCK_TEMPLATE

			# data formatting
			user_input = input('Chain ID: ')
			genesis['config']['chainId'] = formatting(user_input)
			print('Chain ID set to {}'.format(genesis['config']['chainId']))

			user_input = input('Difficulty: ')
			user_input = formatting(user_input)

			if user_input > INT16:
				user_input = INT16

			genesis['difficulty'] = hex(user_input)
			print('Difficulty set to {}'.format(genesis['difficulty']))

			user_input = input('Gas Limit: ')
			user_input = formatting(user_input)

			if user_input > INT16:
				user_input = INT16

			genesis['gasLimit'] = hex(user_input)
			print('Gas Limit set to {}'.format(genesis['gasLimit']))

			print('\n=== Hashing Variables ===')
			genesis['nonce'] = generate_hex_string(16)
			print('Random nonce generated as {}'.format(genesis['nonce']))

			genesis['mixhash'] = generate_hex_string(64)
			print('Random mix hash generated as {}'.format(genesis['mixhash']))

			genesis['parentHash'] = generate_hex_string(64)
			print('Random parent hash generated as {}'.format(genesis['parentHash']))
			
			print('\n=== Generating Genesis Block ===')
			print('Does the following payload look correct?\n')
			pprint.pprint(genesis)
			user_input = input('\n(y/n): ')
			if user_input is 'y':
				break
			print('\n... Throwing away old data and starting fresh ...\n')
		
		# modify if using the --home_dir option or the current working directory (current working directory is the default)
		run_location, filename = os.path.split(os.path.abspath(__file__))
		config = configparser.ConfigParser()
		config.read(os.path.join(run_location, 'config/default.conf'))
		settings.lamden_home = os.environ.get('LAMDEN_HOME', None) if os.environ.get('LAMDEN_HOME', None) else os.getcwd()
		settings.lamden_folder_path = os.environ.get('LAMDEN_FOLDER_PATH', None) if os.environ.get('LAMDEN_FOLDER_PATH', None) else join(settings.lamden_home, project_dir)
		settings.lamden_db_file = os.environ.get('LAMDEN_DB_FILE', None) if os.environ.get('LAMDEN_DB_FILE', None) else join(settings.lamden_folder_path, config.defaults()['lamden_db_file'])
		
		print(settings.lamden_home)
		print(settings.lamden_folder_path)
		print(settings.lamden_db_file)

		try:
		    os.makedirs(settings.lamden_folder_path)
		except OSError as e:
		    pass
		#os.makedirs(project_dir, exist_ok=True)
		#PROJECT_DIR = project_dir
		#os.chdir(project_dir)
		print('Directory created in: {}'.format(os.getcwd()))

		create_genesis_block(genesis)
		print('Genesis block written!')

		print('\n=== Initializing Chain... ===\n')
		initialize_chain(settings.lamden_folder_path, 'genesis.json')
		print('Chain initialized!')

		user_input = input('Enter password for default account: ')
		create_account(user_input)
		print('Blockchain generated!')
	else:
		print('Already in a project directory...')

	#geth.attach(stdout=PIPE, stdin=PIPE)

# this should be added to the account class in some capacity
def create_account(password):
	print(settings.lamden_folder_path)
	with open(os.path.join(settings.lamden_folder_path, 'pass.temp'), 'w') as fp:
		fp.write(password)
	proc = subprocess.Popen('geth --datadir {} --password {} account new'.format(settings.lamden_folder_path, os.path.join(settings.lamden_folder_path, 'pass.temp')), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	account_string = proc.stdout.read().decode('utf-8')
	# return the regex account
	try:
		return re.split(r"\{|\}", account_string)[0]
	except Exception as e:
		try:
			return re.split(r"\{|\}", account_string)[1]
		except Exception as e:
			raise e
	#os.remove('pass.temp')

def close_if_timeout(process, timeout=3000):
	output = b''
	time = 0
	while time < timeout:
		if output == process.stdout.read():
			time += 1
		else:
			output = process.stdout.read()
			time = 0
		# sleep one millisecond
		time.sleep(0.0001)