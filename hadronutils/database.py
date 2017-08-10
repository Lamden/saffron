import sqlite3


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
def init_dbs(sqls):
    for s in sqls:
        try:
            cursor.execute(s)
        except Exception as e:
            if 'already exists' in e.message:
                pass
            else:
                raise e
init_dbs([create_contracts, create_accounts])

def exec_sql(sql):
    try:
        response = cursor.execute(sql)
    except Exception as e:
        return None;
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
        c.name, c.response, c.is_deployed = next(exec_sql(select_from(table=table, name=name, address=address)))
        return c
    except Exception as e:
        raise ValueError('Unable to initialize Contract: \n{e}\n'.format(e=str(e)))

def account_exists(name=None, address=None, table='accounts'):
    name, address = name_or_address(name, address)
    try:
        return next(exec_sql(select_from(table=table, name=name, address=address)))
    except StopIteration:
        return None, None    
    except Exception as e:
        raise e

def init_account(name=None, address=None, table='accounts'):
    try:
        return Account(name=name, address=address)
    except Exception as e:
        import traceback
        t = traceback.format_exc()
        import pdb;pdb.set_trace()
        return ValueError('Unable to initialize Account with values: {name} {address}'.format(name=name, address=address))

def insert_account(name, address):
    assert name, address
    try:
        cursor.execute('INSERT INTO accounts(name, address) VALUES (?, ?)', (name, address))
        connection.commit()
    except sqlite3.IntegrityError as e:
        return 'Account exists'

def insert_contract(contract=None):
    assert contract
    cursor.execute('INSERT INTO contracts VALUES (name "{}", address "{}")'.format(contract.name, contract.address, contract.deployed))


