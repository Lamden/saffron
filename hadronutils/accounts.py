import subprocess
import argparse
import random
import pprint
import json
import os
from web3 import Web3
from web3.personal import Personal

class Account:
	def __init__(self, name=None, password=None, chain=None):
		assert name != None and password != None and chain != None
		# check if name already exists in db. if not, continue
		self.address = chain.web3.personal.newAccount(password)
		self.name = name
		pass

def create_account(password):
	with open('pass.temp', 'w') as fp:
		fp.write(password)
	proc = subprocess.Popen('geth --datadir . --password pass.temp account new', stdout=subprocess.PIPE)
	os.remove('pass.temp')