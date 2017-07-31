import random
import pprint
import json
import subprocess

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
		f = open('config.hadron', 'r')
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

	with open('genesis.json', 'w') as fp:
		json.dump(genesisBlockPayload, fp)

def initialize_chain(project_dir, genesisBlockPath):
	subprocess.Popen('geth --datadir ' + project_dir + ' init ' + genesisBlockPath, shell=True)

def run_generator():
	if not check_if_in_project():
		# create a new chain!
		print('=== Project Name ===')
		project_dir = input('Name your new Hadron project: ')

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

		os.makedirs(project_dir, exist_ok=True)
		PROJECT_DIR = project_dir
		os.chdir(project_dir)
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

def create_account(password):
	with open('pass.temp', 'w') as fp:
		fp.write(password)
	proc = subprocess.Popen('geth --datadir . --password pass.temp account new', stdout=subprocess.PIPE, shell=True)
	os.remove('pass.temp')