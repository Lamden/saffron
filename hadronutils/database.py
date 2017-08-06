import sqlite3

class Database:
    
    def __init__(self, connector='directory.db'):
        self.connection = sqlite3.connect(connector)
        self.cursor = self.connection.cursor()

        # graceful initialization tries to create new tables as a test to see if this is a new DB or not
        try:
            self.cursor.execute('CREATE TABLE accounts (name text primary key, address text)')
            self.cursor.execute('''
                CREATE TABLE contracts ( 
                name text primary key, 
                address text, 
                deployed boolean,
                abi text,
                metadata text,
                gas_estimates blob,
                method_identifiers blob,
                instance blob
                )''')
        except:
            pass

    def select_contract(self, name=None, address=None):
        assert name != None or address != None
        sql = 'SELECT * FROM contracts WHERE'
        if name:
            sql += ' name = "{}"'.format(name)
        if address:
            sql += ' address = "{}"'.format(address)

        try:
            response = self.cursor.execute(sql)
        except Exception as e:
            return None;

        assert len(response) <= 1

        try:
            c = Contract()
            c.name = response[0][0]
            c.response = response[0][1]
            c.is_deployed = response[0][2]
            return c
        except:
            return None

    def select_account(self, name=None, address=None):
        assert name != None or address != None
        
        sql = 'SELECT * FROM accounts WHERE'
        if name:
            sql += ' name = "{}"'.format(name)
        if address:
            sql += ' address = "{}"'.format(address)
        response = self.cursor.execute(sql)

        try:
            response = response.fetchone()[0]
        except:
            return None
        
        try:
            return Account(name=response[0][0], address=response[0][1])
        except:
            return None

    def set_account(self, account=None):
        assert account

        pass
    def set_contract(self, contract=None):
        pass

    def insert_account(self, account=None):
        assert account
        self.cursor.execute('INSERT INTO accounts VALUES ("{}", "{}")'.format(account.name, account.address))

    def insert_contract(self, contract=None):
        assert contract
        self.cursor.execute('INSERT INTO contracts VALUES (name "{}", address "{}")'.format(contract.name, contract.address, contract.deployed))