import sqlite3

class Database:
    
    def __init__(self, connector='directory.db'):
        self.connection = sqlite3.connect(connector)
        self.cursor = self.connection.cursor()

        # graceful initialization tries to create new tables as a test to see if this is a new DB or not
        try:
            self.cursor.execute('CREATE TABLE accounts (id integer primary key, name text, address text)')
            self.cursor.execute('CREATE TABLE contracts (id integer primary key, name text, address text, boolean deployed)')
        except:
            pass

    def get(self, table='accounts', name=None, address=None):
        assert name != None or address != None
        
        sql = 'SELECT * FROM {} WHERE'.format(table)
        
        if name:
            sql += ' name={}'.format(name)
        if address:
            sql += ' address={}'.format(address)

        response = self.cursor.execute(sql)

        assert len(response) <= 1

        try:
            return Account(name=response[0][0], address=response[0][1]) if table=='accounts' else Contract(name=response[0][0], address=response[0][1])
        except:
            return None

    def set_account(self, account=None):
        assert account

        pass
    def set_contract(self, contract=None):
        pass