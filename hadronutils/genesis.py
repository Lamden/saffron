import subprocess
import argparse
import random
import pprint
import json
import os
import accounts
import utils
import sqlite3
from utils import *

class Chain:
	class __Chain:
		def __init__(self, project_dir='.', genesisBlockPayload=None, genesisBlockPath='genesis.json'):
			self.project_dir = project_dir
			self.genesis_block_path = genesisBlockPath

			# initialize chain if it doesn't exist already
			try:
				open('{}/{}'.format(project_dir, genesisBlockPath), 'r')
			except:
				assert genesisBlockPayload, 'Not in a valid project directory or no genesis block payload has been provided.'
				create_genesis_block(genesisBlockPayload)
				initialize_chain(project_dir, genesisBlockPath)

		def start(self):
			self.process = subprocess.Popen('geth --datadir {} --etherbase 0')
			return self.process

		def has_started(self):
			if self.process:
				return True
			return False

	instance = None
	def __init__(self):
		if not Chain.instance:
			Chain.instance = Chain.__Chain()
		#else:
		#	Chain.instance.project_dir = project_dir
	def __getattr__(self, name):
		return getattr(self.instance, name)

class Database:
	def __init__(self, connector='aux_info.db'):
		self.connection = sqlite3.connect(connector)
		self.cursor = self.connection.cursor()

		# graceful initialization tries to create new tables as a test to see if this is a new DB or not
		try:
			self.cursor.execute('CREATE TABLE accounts (id integer primary key, name text, address text)')
			self.cursor.execute('CREATE TABLE contracts (id integer primary key, name text, address text, boolean deployed)')
		except:
			pass

	def get(self, table='accounts', name=None, address=None):
		assert name != None or address != None
		
		sql = 'SELECT * FROM {} WHERE'.format(table)
		
		if name:
			sql += ' name={}'.format(name)
		if address:
			sql += ' address={}'.format(address)

		response = self.cursor.execute(sql)

		assert len(response) <= 1

		try:
			return Account(name=response[0][0], address=response[0][1]) if table=='accounts' else Contract(name=response[0][0], address=response[0][1])
		else:
			return None

	def set_account(self, account=None):
		assert account

		pass
	def set_contract(self, contract=None):
		pass