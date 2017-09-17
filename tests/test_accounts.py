import pytest, os
from saffron.accounts import Account
from saffron.genesis import Chain
from saffron.database import insert_account
from saffron.settings import lamden_folder_path
import uuid

mock_json = b'''{"identity": "GenesisNode", "rpc": true, "rpcport": 8545, "rpccorsdomain": "*", "port": 30303, "nodiscover": false, "ipcapi": "admin,db,eth,debug,miner,net,shh,txpool,personal,web3", "rpcapi": "db,eth,net,web3,personal,web3", "autodag": true, "networkid": 1900}'''

with open(os.path.expanduser('~/node.info'.format(HOME=os.environ.get('HOME'))), 'wb') as f:
    f.write(mock_json)

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
    with open(os.path.join(lamden_folder_path, 'pass.temp')) as f:
        p = f.read()
        assert p == 'testing123'

def test_account_stored_in_db_when_created():
    new_account = str(uuid.uuid1())
    a = Account(name=new_account, password='doesnt_matter', chain=Chain())
    b = Account(name=new_account, password='doesnt_matter', chain=Chain())
    assert a.name == b.name
    assert a._new_account
    # assert b._new_account is False
