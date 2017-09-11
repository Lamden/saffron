import argparse

import configparser
from os.path import join
from saffron import utils
from saffron import settings
from saffron.genesis import Chain
from saffron.contracts import Contract
import os
import click
import subprocess
import uuid
import glob

@click.group()
def cli():
    """This script showcases different terminal UI helpers in Click."""
    pass

@cli.command('init', short_help='initialize a chain')
@click.argument('chain_name', required=True, default='new_chain')
def init(chain_name):
	''' Initialize a new chain within the lamden project folder
		# lamden_db_file
		'/Users/jmunsch/.lamden/lamden-default/lamden-default.sqlite3'

		# settings.lamden_folder_path
		'/Users/jmunsch/.lamden/lamden-default'

		# lamden_home
		'/Users/jmunsch/.lamden'
	'''

	new_path = os.path.join(settings.lamden_home, chain_name)
	try:
		os.makedirs(new_path)
	except Exception as e:
		print(e)
		pass
	os.chdir(new_path)
	db_filename = os.path.join(chain_name, '{}.sqlite3'.format(chain_name))
	settings.lamden_folder_path = new_path
	settings.lamden_db_file = settings.lamden_db_file.replace('lamden-default/lamden-default.sqlite3', db_filename)
	env = settings.env_source(chain_name)
	s = settings.src_string(LAMDEN_HOME=settings.lamden_home,
			LAMDEN_FOLDER_PATH=settings.lamden_folder_path,
			LAMDEN_DB_FILE=settings.lamden_db_file,
			NODE_INFO_JSON=settings.node_info_json(chain_name),
			PROJECT_GENESIS=settings.project_genesis(chain_name))
	with open(env, 'wb') as f:
		f.write(s.encode('utf-8'))
	print('\n############### project dir ###########\n')
	print('New Source File : {}\n'.format(os.path.expanduser('~/.lamden/{c}/{c}.source'.format(c=chain_name))))
	print('###########\n')
	print(s)
	print('###########\n')
	utils.run_generator(chain_name)

@cli.command('start', short_help='starts a chain based on ENV for genesis location')
@click.argument('chain_name', required=True)
def start(chain_name):
	'''Starts a chain given the folder path.

		see: cat ~/.lamden/project-name/project-name.source
	'''
	genesis_payload = None
	try:
		genesis_payload = open(settings.project_genesis(chain_name), 'r').read()
	except:
		raise Exception('Could not start chain. No genesis.json in this directory. Change directories or initialize a new chain.')
	print('Starting chain...')
	chain = Chain()
	proc = chain.start()
	print(proc.pid)
	with open(settings.chain_pid, 'w') as f:
		f.write(str(proc.pid))

@cli.command('stop', short_help='stop the chain')
def stop():
	try:
		# TODO : this isn't going to work for running multiple chains
		BASH = subprocess.check_output(['which','bash'])
		subprocess.Popen(['killall', 'geth'], stderr=subprocess.PIPE)
		subprocess.Popen(['rm', 'nohup.out'], stderr=subprocess.PIPE)
		subprocess.Popen(['rm', 'pass.temp'], stderr=subprocess.PIPE)
		print('All instances of geth stopped.')
	except:
		raise Exception('Could not stop chain.')

@cli.command('deploy', short_help='deploy a contract')
@click.argument('filepath', required=False)
@click.option('--name', '-n', required=False, default=None)
def deploy(filepath, name):
	if not os.path.isdir(os.path.join(settings.lamden_folder_path, 'contracts')):
		raise Exception('Could not find contracts directory. Are you in the project folder?')

	if filepath == None:
		print('Deploying all contracts...')
		# glob it
		sol_files = os.path.join(settings.lamden_folder_path, 'contracts/*.sol')
		filepaths = glob.glob(os.path.abspath(sol_files))
		print(filepaths)
		for fp in filepaths:
			deploy_contract(fp, name)
	else:
		deploy_contract(filepath, name)

def deploy_contract(filepath, name=None):
	if name == None:
		name = str(uuid.uuid1())
	contract = Contract(name, filepath)
	try:
		contract_instance = contract.deploy(cwd=True)
		print('Contract deployed: {}'.format(str(contract_instance)))
	except:
		raise Exception('Could not deploy contract.')

# add new for contracts and addresses
@cli.command('new', short_help='create a new contract')
@click.argument('option', required=False)
@click.option('--name', '-n', required=False, default=None)
def new(option, name):
	assert option != None and option in ['account', 'contract'], 'Provide either "account" or "contract" after "new"'
	if option == 'account':
		print('Generating new account.')

		project_dir = ''
		run_location, filename = os.path.split(os.path.abspath(__file__))
		config = configparser.ConfigParser()
		config.read(os.path.join(run_location, 'config/default.conf'))
		settings.lamden_home = os.getcwd()
		settings.lamden_folder_path = join(settings.lamden_home, project_dir)
		settings.lamden_db_file = join(settings.lamden_folder_path, config.defaults()['lamden_db_file'])

		user_input = input('Enter password for new account: ')
		print(utils.create_account(user_input))
	else:
		print('Generating new contract.')
	pass

# add list for contracts and addresses
@cli.command()
@click.argument('option', required=False)
def list(option):
	assert option != None and option in ['account', 'contract'], 'Provide either "account" or "contract" after "list"'
	pass