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

@cli.command()
def init():
	utils.run_generator()

@cli.command()
def start():
	genesis_payload = None
	try:
		genesis_payload = open(os.path.abspath(os.path.join(os.getcwd(), 'genesis.json')), 'r').read()
	except:
		raise Exception('Could not start chain. No genesis.json in this directory. Change directories or initialize a new chain.')
	
	project_dir = ''
	run_location, filename = os.path.split(os.path.abspath(__file__))
	config = configparser.ConfigParser()
	config.read(os.path.join(run_location, 'config/default.conf'))
	settings.lamden_home = os.environ.get('LAMDEN_HOME', None) if os.environ.get('LAMDEN_HOME', None) else os.getcwd()
	settings.lamden_folder_path = os.environ.get('LAMDEN_FOLDER_PATH', None) if os.environ.get('LAMDEN_FOLDER_PATH', None) else join(settings.lamden_home, project_dir)
	settings.lamden_db_file = os.environ.get('LAMDEN_DB_FILE', None) if os.environ.get('LAMDEN_DB_FILE', None) else join(settings.lamden_folder_path, config.defaults()['lamden_db_file'])

	print('Starting chain...')
	chain = Chain()
	proc = chain.start()
	print(proc.pid)
	with open('.pid', 'w') as f:
		f.write(str(proc.pid))

@cli.command()
def stop():
	try:
		BASH = subprocess.check_output(['which','bash'])
		subprocess.Popen(['killall', 'geth'], stderr=subprocess.PIPE)
		subprocess.Popen(['rm', 'nohup.out'], stderr=subprocess.PIPE)
		subprocess.Popen(['rm', 'pass.temp'], stderr=subprocess.PIPE)
		print('All instances of geth stopped.')
	except:
		raise Exception('Could not stop chain.')

@cli.command()
@click.argument('filename', required=False)
@click.option('--name', '-n', required=False, default=None)
def deploy(filename, name):
	try:
		os.chdir(os.path.join(__file__.replace('cli.py',''), 'contracts'))
	except:
		raise Exception('Could not find contracts directory. Are you in the project folder?')

	if filename == None:
		print('Deploying all contracts...')
		# glob it
		filenames = glob.glob("*.sol")
		for file in filenames:
			deploy_contract(file, name)
	else:
		deploy_contract(filename, name)

def deploy_contract(filename, name=None):
	if name == None:
		name = str(uuid.uuid1())
	contract = Contract(name, filename)
	try:
		contract.deploy()
	except:
		raise Exception('Could not deploy contract.')

# add new for contracts and addresses
@cli.command()
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