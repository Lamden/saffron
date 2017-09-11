import sqlite3
import os, logging
from saffron.settings import lamden_db_file
from contextlib import suppress
import pickle


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
log = logging.getLogger(__file__)
print(lamden_db_file)
connection = sqlite3.connect(lamden_db_file)
cursor = connection.cursor()

def init_dbs(sqls):
    # graceful initialization tries to create new tables as a test to see if this is a new DB or not
    for s in sqls:
        with suppress(sqlite3.OperationalError):
            cursor.execute(s)
init_dbs([create_contracts, create_accounts])

def exec_sql(sql):
    try:
        response = cursor.execute(sql)
    except Exception as e:
        return None;
    return response

def name_or_address(name, address):
    name = ' name = "{}"'.format(name) if name else None
    address = ' address = "{}"'.format(address) if address else None
    assert name != None or address != None
    return name, address

def contract_exists(name=None, address=None, table='contracts'):
    _name, _address = name_or_address(name, address)
    try:
        # XXX: is this a security risk if users are able to submit "name" or "address"
        # XXX: see ? syntax for sql queries for proper escaping
        return next(exec_sql(select_from(table=table, name=_name, address=_address)))
    except StopIteration:
        return None, None
    except Exception as e:
        return None, None

def account_exists(name=None, address=None, table='accounts'):
    _name, _address = name_or_address(name, address)
    try:
        return next(exec_sql(select_from(table=table, name=_name, address=_address)))
    except StopIteration:
        return None, None
    except Exception as e:
        return None, None

def init_account(name=None, address=None, table='accounts'):
    try:
        return Account(name=name, address=address)
    except Exception as e:
        import traceback
        t = traceback.format_exc()
        import pdb;pdb.set_trace()
        return ValueError('Unable to initialize Account with values: '
                          '{name} {address}'.format(name=name, address=address))

def insert_account(name, address):
    assert name, address
    try:
        cursor.execute('INSERT INTO accounts(name, address) VALUES (?, ?)', (name, address))
        connection.commit()
    except sqlite3.IntegrityError as e:
        return 'Account exists'

def update_contract(address, instance, name):
    assert address
    assert instance
    assert name
    result = cursor.execute(update_contracts_sql, (address, pickle.dumps(instance), name))
    return [x for x in cursor.execute('select * from contracts where address=?', (address, ))]

def insert_contract(name: str, abi, bytecode: str, gas_estimates, method_identifiers, cwd):
    '''insert_contract into the localdb, also converts the type
    '''
    assert name
    assert abi
    assert bytecode
    assert gas_estimates
    assert method_identifiers
    gas = pickle.dumps(gas_estimates)
    methods = pickle.dumps(method_identifiers)
    result = cursor.execute(insert_contract_sql, (name,
                                                str(abi),
                                                bytecode,
                                                sqlite3.Binary(gas),
                                                sqlite3.Binary(methods)))
    connection.commit()
    return result


insert_contract_sql = '''
                         INSERT INTO contracts (
                         name,
                         abi,
                         metadata,
                         gas_estimates,
                         method_identifiers) VALUES (?,?,?,?,?)'''

update_contracts_sql = '''
                         UPDATE contracts
                         SET
                         address = ?,
                         instance = ?,
                         deployed = 'true'
                         where name = ? ;'''

input_json = '''{"language": "Solidity","sources": {
                                 "{{name}}": {
                                         "content": {{sol}}
                                 }
                         },
                         "settings": {
                                 "outputSelection": {
                                         "*": {
                                                 "*": [ "metadata", "evm.bytecode", "abi", "evm.bytecode.opcodes", "evm.gasEstimates", "evm.methodIdentifiers" ]
                                         }
                                 }
                         }
               }'''
