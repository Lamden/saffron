import subprocess
import argparse
import random
import pprint
import json
import os

class Account:
	def __init__(self, name=None, address=None):
		self.name = name
		self.address = address
		pass

def create_account(password):
	with open('pass.temp', 'w') as fp:
		fp.write(password)
	proc = subprocess.Popen('geth --datadir . --password pass.temp account new', stdout=subprocess.PIPE)
	os.remove('pass.temp')