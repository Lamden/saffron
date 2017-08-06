# from reconf.location import TestStringLocation as TSL
# from bowie import config
# from bowie.download import proxies
import pytest
import re
from hadronutils.database import Database

def test_tables():
    d = Database()
    assert hasattr(d, 'select_account')
    assert hasattr(d, 'set_account')
    assert hasattr(d, 'select_contract')
    assert hasattr(d, 'connection')
    assert hasattr(d, 'cursor')    

