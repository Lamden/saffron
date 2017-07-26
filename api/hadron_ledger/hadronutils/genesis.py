import subprocess
import argparse
import random
import pprint
import json
import os

def gen_chain():
    parser = argparse.ArgumentParser(description='Hadron CLI tool for Ethereum private networks and side chains.')
    parser.add_argument('-n','--new', help='Create new Ethereum private network.', action='store_true')
    args = parser.parse_args()

    if args.new:
        # create a new chain!
        print('=== Project Name ===')
        user_input = input('Name your new Hadron project: ')
        os.makedirs(user_input, exist_ok=True)
        PROJECT_DIR = user_input
        os.chdir(user_input)
        print('Directory created in: {}'.format(os.getcwd()))

        while True:
            print('\n=== Blockchain Settings ===')
            genesis = {
                'config': {
                    'chainId': 0,
                    'homesteadBlock': 0,
                    'eip155Block': 0,
                    'eip158Block': 0
                    },
                'alloc'      : {},
                'coinbase'   : '0x0000000000000000000000000000000000000000',
                'difficulty' : '0x0',
                'extraData'  : '',
                'gasLimit'   : '0x0',
                'nonce'      : '0x0000000000000000',
                'mixhash'    : '0x0000000000000000000000000000000000000000000000000000000000000000',
                'parentHash' : '0x0000000000000000000000000000000000000000000000000000000000000000',
                'timestamp'  : '0x00'
                }

            alloc_account = { '0x0000000000000000000000000000000000000000': {'balance': '0'} }

            # data formatting
            def formatting(i):
                try:
                    i = int(i)
                except:
                    i = 0

                if i < 0:
                    i = 0
                return i

            INT16 = 18446744073709551615

            user_input = input('Chain ID: ')
            user_input = formatting(user_input)
            genesis['config']['chainID'] = user_input
            print('Chain ID set to {}'.format(user_input))

            user_input = input('Difficulty: ')
            user_input = formatting(user_input)

            if user_input > INT16:
                user_input = INT16

            genesis['difficulty'] = hex(user_input)
            print('Difficulty set to {}'.format(hex(user_input)))

            user_input = input('Gas Limit: ')
            user_input = formatting(user_input)

            if user_input > INT16:
                user_input = INT16

            genesis['gasLimit'] = hex(user_input)
            print('Gas Limit set to {}'.format(hex(user_input)))

            def generate_hex_string(length):
                string = '0x'
                for i in range(length):
                    string += hex(random.randint(0, 16))[-1]
                return string

            print('\n=== Hashing Variables ===')
            nonce = generate_hex_string(16)
            genesis['nonce'] = nonce
            print('Random nonce generated as {}'.format(nonce))

            nonce = generate_hex_string(64)
            genesis['mixhash'] = nonce
            print('Random mix hash generated as {}'.format(nonce))

            nonce = generate_hex_string(64)
            genesis['parentHash'] = nonce
            print('Random parent hash generated as {}'.format(nonce))
            print('\n=== Initial Accounts ===')
            while True:
                user_input = input('Create a new initial account? (y/n): ')
                if user_input is not 'y':
                    break

                new_account = generate_hex_string(40)

                user_input = input('Enter initial balance: ')
                user_input = formatting(user_input)

                if user_input > INT16:
                    user_input = INT16

                genesis['alloc'][new_account] = { 'balance' : str(user_input) }
                print('New initial account created with address {} and balance {}'.format(new_account, user_input))

            print('\n=== Generating Genesis Block ===')
            print('Does the following payload look correct?\n')
            pprint.pprint(genesis)
            user_input = input('\n(y/n): ')
            if user_input is 'y':
                break
            print('\n... Throwing away old data and starting fresh ...\n')

        with open('genesis.json', 'w') as fp:
            json.dump(genesis, fp)
        print('Genesis block written!')

        print('\n=== Initializing Chain... ===\n')
        print(os.popen("geth --datadir . init genesis.json").read())
        print('\nChain initialized!')
