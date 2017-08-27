import os

import sqlite3
from web3 import Web3, KeepAliveRPCProvider
import web3

from saffron import database
from saffron.settings import lamden_home

import subprocess

from saffron.utils import create_genesis_block, initialize_chain, create_account, GENESIS_BLOCK_TEMPLATE

class MemoizedChain:
	class __Chain:
		def __init__(self, project_dir='.', genesis_block_payload=None, genesis_block_path='genesis.json', cwd=True):
			self.project_dir = project_dir if cwd else lamden_home
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
			GETH = subprocess.check_output(['which','geth'])
			#pid = os.spawnlp(os.P_NOWAITO, GETH.strip(), 'geth','--datadir',self.project_dir, '--etherbase','0', '&')
			proc = subprocess.Popen(['nohup', GETH.strip(), 'geth --datadir {} --etherbase 0'.format(self.project_dir)])
			return proc

		def stop(self):
			self.process.terminate()
			return self.process.poll()

		def has_started(self):
			if self.process:
				return True
			return False

	instance = None
	def __init__(self, project_dir='.', genesis_block_payload=None, genesis_block_path='genesis.json', cdw=True):
		if not Chain.instance:
			Chain.instance = Chain.__Chain(project_dir, genesis_block_payload, genesis_block_path)
		#else:
		#	Chain.instance.project_dir = project_dir
	def __getattr__(self, name):
		return getattr(self.instance, name)

Chain = MemoizedChain