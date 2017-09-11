import os

import sqlite3
from web3 import Web3, KeepAliveRPCProvider
import web3

from saffron import database
from saffron.settings import lamden_home, project_genesis
import subprocess

from saffron.utils import create_genesis_block, initialize_chain, create_account, GENESIS_BLOCK_TEMPLATE, generate_process_string

class MemoizedChain:
	class __Chain:
		def __init__(self, project_dir=None, genesis_block_payload=None, genesis_block_path=project_genesis, cwd=True):
			self.genesis_block_path = genesis_block_path
			self.database = database

		def start(self):
			GETH = subprocess.check_output(['which','geth'])
			geth_string = generate_process_string()
			print(geth_string)
			proc = subprocess.Popen(['nohup', GETH.strip()] + geth_string.split())
			return proc

		def stop(self):
			self.process.terminate()
			return self.process.poll()

		def has_started(self):
			if self.process:
				return True
			return False

	instance = None
	def __init__(self, project_dir=None, genesis_block_payload=None, genesis_block_path='genesis.json', cwd=True):
		if not Chain.instance:
			project_dir = lamden_home
			Chain.instance = Chain.__Chain(project_dir, genesis_block_payload, genesis_block_path)
		#else:
		#	Chain.instance.project_dir = project_dir
	def __getattr__(self, name):
		return getattr(self.instance, name)

Chain = MemoizedChain