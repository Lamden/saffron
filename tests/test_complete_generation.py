import os
import pytest
from saffron.genesis import Chain
from saffron.accounts import *
import uuid


"""
	workflow is...

	hadron init
	
	create a new account
		=> creates a new account object
		=> adds it to the database
		=> adds it to the blockchain

	query accounts from database
	
	query accounts from blockchain

	query specific address (by name in db to blockchain)

	create a new contract
		=> creates a new contract object
		=> adds it to the database
		=> deploys on block chain when user says so

	query contract from database
	query contract from blockchain

	query specific contract
		=> create a new contract object
		=> load it with a .tsol file
		=> woohoo
		(same for a .sol)
"""
# import os
# dir = os.path.dirname(__file__)
# filename = os.path.join(dir, '/relative/path/to/file/you/want')

# make a test directory to create a project in and delete after tests

test_genesis_block = {'alloc': {},
 'coinbase': '0x0000000000000000000000000000000000000000',
 'config': {'chainId': 0,
            'eip155Block': 0,
            'eip158Block': 0,
            'homesteadBlock': 0},
 'difficulty': '0xfa0',
 'extraData': '',
 'gasLimit': '0x3b9aca00',
 'mixhash': '0x60435bb94315636abf20c56b94ef172f55f90f4b55910a456866d389fe75c5c2',
 'nonce': '0x136927a0155972f0',
 'parentHash': '0x1f05d1e4d4a5b6556cb10b426eca46e8f9a374c7793f307928c39b88b084726e',
 'timestamp': '0x00'}

chain = Chain(genesis_block_payload=test_genesis_block)