import os

import sqlite3
from web3 import Web3, KeepAliveRPCProvider
import web3

from hadronutils.utils import create_genesis_block, initialize_chain, create_account, GENESIS_BLOCK_TEMPLATE
from hadronutils import database
from hadronutils.settings import WORKING_DIR

class MemoizedChain:
	class __Chain:
		def __init__(self, project_dir='', genesis_block_payload=None, genesis_block_path='genesis.json'):
			self.project_dir = WORKING_DIR
			self.genesis_block_path = genesis_block_path
			database.init_dbs([database.create_contracts, database.create_accounts])
			self.database = database
			# initialize chain if it doesn't exist already
			try:
				open(os.path.join(self.project_dir, genesis_block_path), 'r')
			except:
				assert genesis_block_payload, 'No payload given'
				# if genesis_block_payload == None:
					# genesis_block_payload = GENESIS_BLOCK_TEMPLATE
				create_genesis_block(genesis_block_payload)
				initialize_chain(self.project_dir, genesis_block_path)
				create_account('password')

		def start(self):
			self.process = subprocess.Popen('geth --datadir {} --etherbase 0'.format(self.project_dir), shell=True)
			import pdb;pdb.set_trace()
			self.process.pid
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

Chain = MemoizedChain