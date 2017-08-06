import pytest
from hadronutils.accounts import *
from hadronutils.genesis import *
from hadronutils.database import *
import uuid

@pytest.fixture
def chain(monkeypatch): # monkeypatch is magically injected
    class Chain(object):
        lines = []

        def __init__(self, *args, **kwargs):
            pass

        def read(self, *args, **kwargs):
            try:
                return self.lines.pop()
            except:
                return 'hmm'
    # monkeypatch.setattr( 'some.Example', Example)
    return Chain()

def test_accounts(chain):
    a = Account.new(name='hello', password='testing123', chain=chain)
    assert hasattr(a, 'address'), 'No address'
    assert hasattr(a, 'name'), 'No name'

def test_account_stored_in_db_when_created():
    a = Account.new(name=str(uuid.uuid1()), password='doesnt_matter', chain=Chain())
    #b = Chain().database.cursor.execute('''SELECT * FROM accounts WHERE name = "{}"'''.format(a.name))
    #print(b.fetchone()[0])
    b = Account.from_db(name=a.name)

    assert a != None, 'New Account not created'
    assert b != None, 'New Account not pulled from the db'
    assert a.name == b.name, 'Names are not equal'
    assert a.address == b.address, 'Address are not equal'