import pytest
from hadronutils.accounts import Account
# from hadronutils.genesis import Chain

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