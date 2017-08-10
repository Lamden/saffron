# from reconf.location import TestStringLocation as TSL
# from bowie import config
# from bowie.download import proxies
import pytest
import re
from hadronutils import database

def test_tables():
    d = database
    assert hasattr(d, 'account_exists')
    assert hasattr(d, 'connection')
    assert hasattr(d, 'contract_exists')
    assert hasattr(d, 'create_accounts')
    assert hasattr(d, 'create_contracts')
    assert hasattr(d, 'cursor')
    assert hasattr(d, 'exec_sql')
    assert hasattr(d, 'init_account')
    assert hasattr(d, 'init_dbs')
    assert hasattr(d, 'insert_account')
    assert hasattr(d, 'insert_contract')
    assert hasattr(d, 'name_or_address')
    assert hasattr(d, 'select_from')
    assert hasattr(d, 'sqlite3')

