import subprocess
import argparse
import random
import pprint
import json
import os
from web3 import Web3
from web3.personal import Personal
import utils

class Account:
	def __init__(self, name=None, password=None, chain=None):
		assert name != None and password != None and chain != None
		# check if name already exists in db. if not, continue
		self.address = utils.create_account(password)
		self.name = name
