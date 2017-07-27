import subprocess
import argparse
import random
import pprint
import json
import os

parser = argparse.ArgumentParser(description='Hadron CLI tool for Ethereum private networks and side chains.')
parser.add_argument('new', help='Create new Ethereum private network.', action='store_true')
args = parser.parse_args(allow_abbrev=False)
print(args)

