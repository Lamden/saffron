import argparse
from hadronutils import utils
from hadronutils import settings
from hadronutils.genesis import Chain
import os
import click

# parser = argparse.ArgumentParser()
# subparsers = parser.add_subparsers()

# init_parser = subparsers.add_parser('init')
# init_parser.set_defaults(func=init)

# start_parser = subparsers.add_parser('start')
# start_parser.set_defaults(func=start)

# stop_parser = subparsers.add_parser('stop')
# connect_parser = subparsers.add_parser('connect')

# def main():
#     args = parser.parse_args()
#     args.func(args)

@click.group()
def cli():
    """This script showcases different terminal UI helpers in Click."""
    pass

@cli.command()
def init(args):
	utils.run_generator()


@cli.command()
def start(args):
	settings.create_working_dir(os.getcwd())
	genesis_payload = None
	try:
		genesis_payload = open(os.path.abspath(os.path.join(settings.WORKING_DIR, 'genesis.json')), 'r').read()
	except:
		raise Exception('Could not start chain. No genesis.json in this directory. Change directories or initialize a new chain.')
	Chain().start()