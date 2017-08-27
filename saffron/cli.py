import argparse
from saffron import utils
from saffron import settings
from saffron.genesis import Chain
import os
import click
import subprocess

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
