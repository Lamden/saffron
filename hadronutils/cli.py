import argparse
from hadronutils import utils
from hadronutils import settings
from hadronutils.genesis import Chain
import os
import click

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
		genesis_payload = open(os.path.abspath(os.path.join(settings.WORKING_DIR, 'genesis.json')), 'r').read()
	except:
		raise Exception('Could not start chain. No genesis.json in this directory. Change directories or initialize a new chain.')
	Chain().start()