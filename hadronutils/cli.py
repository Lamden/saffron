import argparse
from hadronutils import utils
from hadronutils import settings
from hadronutils.genesis import Chain
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
		os.chdir(os.path.join(os.getcwd(), '/contracts'))
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