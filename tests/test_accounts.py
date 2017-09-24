import pytest, os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import socket
from threading import Thread

from saffron.accounts import Account
from saffron.genesis import Chain
from saffron.database import insert_account
from saffron.settings import lamden_folder_path
import uuid

mock_json = b'''{"identity": "GenesisNode", "rpc": true, "rpcport": 8545, "rpccorsdomain": "*", "port": 30303, "nodiscover": false, "ipcapi": "admin,db,eth,debug,miner,net,shh,txpool,personal,web3", "rpcapi": "db,eth,net,web3,personal,web3", "autodag": true, "networkid": 1900}'''

with open(os.path.expanduser('~/node.info'), 'wb') as f:
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



class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        return

    def do_POST(self, *args, **kwargs):
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        if post_body == b'{"jsonrpc": "2.0", "method": "personal_newAccount", "params": ["doesnt_matter"], "id": 0}':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            response_content = json.dumps({"result": ''})
            self.wfile.write(response_content.encode('utf-8'))
            return

def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 8545))
    address, port = s.getsockname()
    s.close()
    return port

def start_mock_server(port):
    mock_server = HTTPServer(('127.0.0.1', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()

start_mock_server(8545)


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

# def test_importRawKey(chain):
#     new_account = str(uuid.uuid1())
#     p = 'doesnt_matter'
#     a = Account(name=new_account, password=p, chain=Chain())
#     private_key = 'asdf'
#     a.p.importRawKey(private_key, p)

def test_newAccount(chain):
    new_account = str(uuid.uuid1())
    p = 'doesnt_matter'
    a = Account(name=new_account, password=p, chain=Chain())
    a.p.newAccount(password=p)

def test_listAccounts(chain):
    new_account = str(uuid.uuid1())
    a = Account(name=new_account, password='doesnt_matter', chain=Chain())
    a.p.listAccounts()

# def test_getListAccounts(chain):
#     new_account = str(uuid.uuid1())
#     a = Account(name=new_account, password='doesnt_matter', chain=Chain())
#     a.p.getListAccounts(*args, **kwargs)

# def test_sendTransaction(chain):
#     new_account = str(uuid.uuid1())
#     a = Account(name=new_account, password='doesnt_matter', chain=Chain())
#     a.p.sendTransaction(transaction, passphrase)

# def test_signAndSendTransaction(chain):
#     new_account = str(uuid.uuid1())
#     a = Account(name=new_account, password='doesnt_matter', chain=Chain())
#     a.p.signAndSendTransaction()

# def test_lockAccount(chain):
#     new_account = str(uuid.uuid1())
#     a = Account(name=new_account, password='doesnt_matter', chain=Chain())
#     a.p.unlockAccount(account, passphrase, duration=None)

# def test_unlockAccount(chain):
#     new_account = str(uuid.uuid1())
#     a = Account(name=new_account, password='doesnt_matter', chain=Chain())
#     a.p.unlockAccount()

# def test_sign(chain):
#     new_account = str(uuid.uuid1())
#     a = Account(name=new_account, password='doesnt_matter', chain=Chain())
#     a.p.sign(message, signer, passphrase)

# def test_ecRecover(chain):
#     new_account = str(uuid.uuid1())
#     a = Account(name=new_account, password='doesnt_matter', chain=Chain())
#     a.p.ecRecover(self, message, signature)