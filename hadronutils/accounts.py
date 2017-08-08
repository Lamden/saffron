import subprocess
import argparse
import random
import pprint
import json
import os
from web3 import Web3
from web3.personal import Personal
from web3.eth import Eth
from hadronutils.utils import create_account
from hadronutils.genesis import Chain

def from_db(name=None, address=None):
	assert name != None or address != None, 'Supply either a name or an address to query the DB with'
	print('{}, {}'.format(address, name))
	a = Chain().database.select_account(name=name, address=address)
	return a


class Account:
	def __init__(self, name=None, address=None, password=None, chain=None):
		assert Chain().database.select_account(name) is None, 'Account with the same name already exists in the database'
		self.name = name
		self.address = create_account(password)
		Chain().database.insert_account(self)

	@classmethod
	def _from_db(self, name, address):
		return from_db(name, address)

	#TODO
	#fancy shit making interacting with the blockchain easy (get balance, transact, etc)
	def balance(self):
		return Eth.get_balance(self.address)