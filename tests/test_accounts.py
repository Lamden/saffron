import pytest, os
from saffron.accounts import Account
from saffron.genesis import Chain
from saffron.database import insert_account
from saffron.settings import hadron_folder_path
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
    new_account = str(uuid.uuid1())
    a = Account(name=new_account, password='testing123', chain=chain)
    assert hasattr(a, 'address'), 'No address'
    assert hasattr(a, 'balance'), 'No balance'
    assert hasattr(a, 'name'), 'No name'
    with open(os.path.join(hadron_folder_path, 'pass.temp')) as f:
        p = f.read()
        assert p == 'testing123'

def test_account_stored_in_db_when_created():
    new_account = str(uuid.uuid1())
    a = Account(name=new_account, password='doesnt_matter', chain=Chain())
    b = Account(name=new_account, password='doesnt_matter', chain=Chain())
    assert a._new_account
    assert not b._new_account