import subprocess
import argparse
import random
import pprint
import json
import os
from web3 import Web3
from web3.personal import Personal
from web3.eth import Eth
from hadronutils.utils import *
from hadronutils.genesis import *

class Account:
	def __init__(self, name=None, address=None):
		self.name = name
		self.address = address

	@classmethod
	def new(self, name=None, password=None, chain=None):
		assert name != None and password != None and chain != None, 'Missing information needed to create an account'
		# check if name already exists in db. if not, continue
		assert Chain().database.select_account(name) is None, 'Account with the same name already exists in the database'
		address = create_account(password)
		
		a = Account(name=name, address=address)

		print('{}, {}'.format(a.address, a.name))

		Chain().database.insert_account(a)
		return a

	@classmethod
	def from_db(self, name=None, address=None):
		assert name != None or address != None, 'Supply either a name or an address to query the DB with'
		print('{}, {}'.format(address, name))
		a = Chain().database.select_account(name=name, address=address)
		return a
		
	#TODO
	#fancy shit making interacting with the blockchain easy (get balance, transact, etc)
	def balance(self):
		return Eth.get_balance(self.address)