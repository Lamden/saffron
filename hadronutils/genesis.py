import os
import accounts
import sqlite3
from web3 import Web3, KeepAliveRPCProvider
import web3
from hadronutils.utils import *
from hadronutils.database import *

class Chain:
	class __Chain:
		def __init__(self, project_dir='.', genesis_block_payload=None, genesis_block_path='genesis.json'):
			self.project_dir = project_dir
			self.genesis_block_path = genesis_block_path
			self.database = Database()
			# initialize chain if it doesn't exist already
			try:
				open('{}/{}'.format(project_dir, genesis_block_path), 'r')
			except:
				assert genesis_block_payload, 'Not in a valid project directory or no genesis block payload has been provided.'
				create_genesis_block(genesis_block_payload)
				initialize_chain(project_dir, genesis_block_path)
				create_account('password')

		def start(self):
			self.process = subprocess.Popen('geth --datadir {} --etherbase 0'.format(self.project_dir), shell=True)
			#self.web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
			return self.process

		def stop(self):
			self.process.terminate()
			return self.process.poll()

		def has_started(self):
			if self.process:
				return True
			return False

	instance = None
	def __init__(self, project_dir='.', genesis_block_payload=None, genesis_block_path='genesis.json'):
		if not Chain.instance:
			Chain.instance = Chain.__Chain(project_dir, genesis_block_payload, genesis_block_path)
		#else:
		#	Chain.instance.project_dir = project_dir
	def __getattr__(self, name):
		return getattr(self.instance, name)