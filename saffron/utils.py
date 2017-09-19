import random
import pprint
import json
import subprocess
import os
import time
from threading import Thread
import re
from saffron.settings import (lamden_home,
							lamden_folder_path,
							lamden_db_file,
							project_genesis,
							GETH_BIN,
							genesis_fn,
							node_info_json)
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
	'difficulty' : '2100000',
	'extraData'  : '',
	'gasLimit'   : '0x8000000',
	'nonce'      : '0x0000000000000000',
	'mixhash'    : '0x0000000000000000000000000000000000000000000000000000000000000000',
	'parentHash' : '0x0000000000000000000000000000000000000000000000000000000000000000',
	'timestamp'  : '0x00'
}

NODE_INFO_TEMPLATE = {
	'identity' : 'GenesisNode',
	'rpc' : True,
	'rpcport' : 8001,
	'rpccorsdomain' : '*',
	'port' : 30303,
	'nodiscover' : True,
	'ipcapi' : 'admin,db,eth,debug,miner,net,shh,txpool,personal,web3',
	'rpcapi' : 'db,eth,net,web3,personal,web3',
	'autodag' : True,
	'networkid' : 1900
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

def create_genesis_block(genesisBlockPayload=None):
	''' places genesis json into os.environ['LAMDEN_FOLDER_PATH']
	'''
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
	with open(os.path.join(os.environ['LAMDEN_FOLDER_PATH'], 'genesis.json'), 'w') as fp:
		json.dump(genesisBlockPayload, fp)

def create_node_info(nodeInfoPayload=None):
	''' places node info json into os.environ['LAMDEN_FOLDER_PATH']
	'''
	assert all(x in \
	['identity',
	'rpc',
	'rpcport',
	'rpccorsdomain',
	'port',
	'nodiscover',
	'ipcapi',
	'rpcapi',
	'autodag',
	'networkid'] \
	for x in list(nodeInfoPayload.keys()))
	with open(os.path.join(os.environ['LAMDEN_FOLDER_PATH'], 'node.info'), 'w') as fp:
		json.dump(nodeInfoPayload, fp)

def initialize_chain(project_dir, genesisBlockFp):
	cmd = '{} --datadir {} init {}'.format(GETH_BIN, os.environ['LAMDEN_FOLDER_PATH'], os.environ['PROJECT_GENESIS'])
	print(cmd)
	result = subprocess.check_output(cmd.split())
	print(result)

def run_generator(chain_name):
	os.environ['LAMDEN_FOLDER_PATH'] = os.path.join(lamden_home, chain_name)
	os.environ['PROJECT_GENESIS'] = project_genesis(chain_name)
	os.environ['NODE_INFO_JSON'] = node_info_json(chain_name)
	if not check_if_in_project():
		# create a new chain!
		# print('=== config {} ==='.format(chain_name))
		node_info = NODE_INFO_TEMPLATE
		while True:
			print('\n=== Network Settings ===')
			node_info = NODE_INFO_TEMPLATE

			user_input = input('Master Node Identity (optional, default = MasterNode): ')
			node_info['identity'] = user_input if user_input else node_info['identity']

			user_input = input('RPC Port (optional, default = 8001): ')
			node_info['rpcport'] = formatting(user_input) if formatting(user_input) > 0 else node_info['rpcport']

			user_input = input('General Port (optional, default = 30303): ')
			node_info['port'] = formatting(user_input) if formatting(user_input) > 0 else node_info['port']

			user_input = input('Network ID (required, default = 1900): ')
			node_info['networkid'] = formatting(user_input) if formatting(user_input) > 0 else node_info['networkid']

			user_input = input('Allow public discovery? (required, default = false) (y/n): ')
			node_info['nodiscover'] = False if user_input == 'y' else node_info['nodiscover']

			user_input = input('Autodag? (required, default = true) (y/n): ')
			node_info['autodag'] = True if user_input == 'y' else node_info['autodag']

			print('Does the following payload look correct?\n')
			pprint.pprint(node_info)
			user_input = input('\n(y/n): ')
			if user_input is 'y':
				break
			print('\n... Throwing away old data and starting fresh ...\n')

		while True:
			print('\n=== Blockchain Settings ===')
			genesis = GENESIS_BLOCK_TEMPLATE

			# data formatting
			user_input = input('Chain ID: ')
			genesis['config']['chainId'] = formatting(user_input)
			print('Chain ID set to {}'.format(genesis['config']['chainId']))

			# user_input = input('Difficulty: ')
			# user_input = formatting(user_input)

			# if user_input > INT16:
			# 	user_input = INT16

			# genesis['difficulty'] = hex(user_input)
			# print('Difficulty set to {}'.format(genesis['difficulty']))

			# user_input = input('Gas Limit: ')
			# user_input = formatting(user_input)

			# if user_input > INT16:
			# 	user_input = INT16

			# genesis['gasLimit'] = hex(user_input)
			# print('Gas Limit set to {}'.format(genesis['gasLimit']))

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

		user_input = input('Enter password for default account: ')
		try:
			new_chain(node_info=node_info, genesis_block=genesis, etherbase_pass=user_input)
		except Exception as e:
			print(e)
			pass
		print('Blockchain generated!')

		# print(generate_process_string())
	else:
		print('Already in a project directory...')

# this should be added to the account class in some capacity
def create_account(password):
	with open(os.path.join(os.environ['LAMDEN_FOLDER_PATH'], 'pass.temp'), 'w') as fp:
		fp.write(password)
	proc = subprocess.Popen('geth --datadir {} --password {} account new'.format(os.environ['LAMDEN_FOLDER_PATH'], os.path.join(os.environ['LAMDEN_FOLDER_PATH'], 'pass.temp')), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def generate_process_string():
	assert open(os.environ.get('PROJECT_GENESIS', None)), 'PROJECT_GENESIS not found in ENV'
	assert open(os.environ.get('NODE_INFO_JSON', None)), 'NODE_INFO_JSON not found in ENV'
	node_info = json.loads(open(os.environ['NODE_INFO_JSON']).read())
	process_string = ''
	process_string += ' --rpc --rpcaddr 0.0.0.0 --rpcport {} --rpccorsdomain "*"'.format(node_info['rpcport']) if node_info['rpc'] else ''
	process_string += ' --datadir {}'.format(os.environ['LAMDEN_FOLDER_PATH'])
	process_string += ' --port {}'.format(node_info['port'])
	process_string += ' --nodiscover' if node_info['nodiscover'] == True else ''
	process_string += ' --rpcapi "{}"'.format(node_info['rpcapi'])
	process_string += ' --networkid {}'.format(node_info['networkid'])
	process_string += ' --gasprice 0 --mine'
	return process_string

def new_chain(node_info=None, genesis_block=None, etherbase_pass=None):
	assert etherbase_pass != None, 'Password for Etherbase account must be provided.'

	if node_info == None:
		node_info = NODE_INFO_TEMPLATE
	if genesis_block == None:
		genesis_block = GENESIS_BLOCK_TEMPLATE
	try:
		os.makedirs(join(os.environ['LAMDEN_FOLDER_PATH'], 'contracts'))
	except:
		pass
	try:
		create_node_info(node_info)
		create_genesis_block(genesisBlockPayload=genesis_block)
		initialize_chain(os.environ['LAMDEN_FOLDER_PATH'], os.environ['PROJECT_GENESIS'])
		create_account(etherbase_pass)
	except Exception as e:
		import traceback
		print(traceback.format_exc())
		raise e