import sqlite3
from hadronutils.accounts import *


create_accounts = 'CREATE TABLE accounts (name text primary key, address text)'

create_contracts = '''
                CREATE TABLE contracts ( 
                name text primary key, 
                address text, 
                deployed boolean,
                abi text,
                metadata text,
                gas_estimates blob,
                method_identifiers blob,
                instance blob
                )'''

select_from = 'SELECT * FROM {table} WHERE {name} {address}'.format

connection = sqlite3.connect('directory.db')
cursor = connection.cursor()

# graceful initialization tries to create new tables as a test to see if this is a new DB or not
try:
    cursor.execute(create_table)
    cursor.execute(create_contracts)
except:
    pass

def exec(sql):
    try:
        response = cursor.execute(sql)
    except Exception as e:
        return None;

    assert len(response) <= 1
    return response

def name_or_address(name, address):
    name = ' name = "{}"'.format(name) if name else ''
    address = ' address = "{}"'.format(address) if address else ''
    assert name != None or address != None
    return name, address

def init_contract(name=None, address=None, table='contracts'):
    name, address = name_or_address(name, address)
    try:
        c = Contract()
        # XXX: is this a security risk if users are able to submit "name" or "address"
        # XXX: see ? syntax for sql queries for proper escaping
        c.name, c.response, c.is_deployed = next(exec(select_from(table=table, name=name, address=address)))
        return c
    except Exception as e:
        raise ValueError('Unable to initialize Contract: \n{e}\n'.format(e=str(e)))

def init_account(name=None, address=None, table='accounts'):
    name, address = name_or_address(name, address)
    try:
        _id, name, address = next(exec(select_from(table=table, name=name, address=address)))
    except Exception as e:
        raise ValueError('Unable to find Account with values: {name} {address}'.format(name=name, address=address))
    try:
        return Account(name=name, address=address)
    except Exception as e:
        return ValueError('Unable to initialize Account with values: {name} {address}'.format(name=name, address=address))

def insert_account(name, address):
    assert name, address
    cursor.execute('INSERT INTO accounts(name, address) VALUES (?, ?)', (name, address))
    connection.commit()

def insert_contract(contract=None):
    assert contract
    cursor.execute('INSERT INTO contracts VALUES (name "{}", address "{}")'.format(contract.name, contract.address, contract.deployed))


