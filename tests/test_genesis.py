import subprocess
import argparse
import random
import pprint
import json
import os

from saffron.genesis import Chain
from saffron.utils import *
from saffron.accounts import Account

test_genesis_block = {'alloc': {},
 'coinbase': '0x0000000000000000000000000000000000000000',
 'config': {'chainId': 123,
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

def test_chain():
    chain = Chain(genesis_block_payload=test_genesis_block)
    assert hasattr(chain, '_MemoizedChain__Chain')
    assert hasattr(chain._MemoizedChain__Chain, 'has_started')
    assert hasattr(chain._MemoizedChain__Chain, 'start')
    assert hasattr(chain._MemoizedChain__Chain, 'stop')
