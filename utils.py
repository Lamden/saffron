GENESIS_BLOCK_TEMPLATE = {
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

INT16 = 18446744073709551615

def check_if_in_project():
	try:
		f = open('config.hadron', 'r')
		return True
	except:
		return False

def formatting(i):
	try:
		i = int(i)
	except:
		i = 0

	if i < 0:
		i = 0
	return i

def generate_hex_string(length):
	string = '0x'
	for i in range(length):
		string += hex(random.randint(0, 16))[-1]
	return string