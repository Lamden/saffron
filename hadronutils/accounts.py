import subprocess
import argparse
import random
import pprint
import json
import os
from web3 import Web3
from web3.personal import Personal
from web3 import Eth
import utils

class Account:
	@classmethod
	def new(self, name=None, password=None, chain=None):
		assert name != None and password != None and chain != None
		# check if name already exists in db. if not, continue
		assert Chain().database.select_account(name) is None
		address = utils.create_account(password)
		
		a = Account()
		a.address = address
		a.name = name

		Chain().database.insert_account(a)

	#TODO
	#fancy shit making interacting with the blockchain easy (get balance, transact, etc)
	def balance(self):
		return Eth.get_balance(self.address)
