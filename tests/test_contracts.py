# from reconf.location import TestStringLocation as TSL
# from bowie import config
# from bowie.download import proxies
import pytest
import re
from hadronutils import contracts

Contract = contracts.Contract

sol_contract = u'''
pragma solidity {{solidity_version}};

contract {{contract_name}} {
    string public constant symbol = "{{symbol}}";
    string public constant asset_name = "{{asset_name}}";
    uint8 public constant decimals = {{decimals}};
    uint256 _totalSupply = {{_totalSupply}};

    address public owner;
 
    mapping(address => uint256) balances;
 
    mapping(address => mapping (address => uint256)) allowed;
 
    modifier onlyOwner() {
        if (msg.sender != owner) {
            throw;
        }
        _;
    }
 
    function FixedSupplyToken() {
        owner = msg.sender;
        balances[owner] = _totalSupply;
    }
 
    function totalSupply() constant returns (uint256 totalSupply) {
        totalSupply = _totalSupply;
    }
 
    function balanceOf(address _owner) constant returns (uint256 balance) {
        return balances[_owner];
    }
 
    function transfer(address _to, uint256 _amount) returns (bool success) {
        if (balances[msg.sender] >= _amount 
            && _amount > 0
            && balances[_to] + _amount > balances[_to]) {
            balances[msg.sender] -= _amount;
            balances[_to] += _amount;
            Transfer(msg.sender, _to, _amount);
            return true;
        } else {
            return false;
        }
    }

    function transferFrom(
        address _from,
        address _to,
        uint256 _amount
    ) returns (bool success) {
        if (balances[_from] >= _amount
            && allowed[_from][msg.sender] >= _amount
            && _amount > 0
            && balances[_to] + _amount > balances[_to]) {
            balances[_from] -= _amount;
            allowed[_from][msg.sender] -= _amount;
            balances[_to] += _amount;
            Transfer(_from, _to, _amount);
            return true;
        } else {
            return false;
        }
    }

    function approve(address _spender, uint256 _amount) returns (bool success) {
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }
 
    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
}
'''


def test_contracts():
    c = Contract()
    assert hasattr(c, 'name')
    assert hasattr(c, 'is_deployed')
    assert hasattr(c, 'address')
    assert hasattr(c, 'abi')
    assert hasattr(Contract(), 'get_template_variables')
    assert hasattr(Contract(), 'generate_new_contract')
    assert c.name == None
    assert c.is_deployed == None
    assert c.address == None


def test_get_template_variables():
    from io import StringIO
    c = Contract()
    var_names = c.get_template_variables(StringIO(sol_contract))
    assert var_names == ['solidity_version', 'contract_name', 'symbol', 'asset_name', 'decimals', '_totalSupply']


def test_generate_new_contract():
    'symbol', 'name', 'decimals', '_totalSupply'
    payload = {'asset_name': 'TEST',
    'contract_name': 'Something',
    'solidity_version': '^0.4.11',
    'decimals': 18,
    'symbol': 'TST',
    '_totalSupply': 100000000000000000000000,
    'sol': sol_contract}
    c = Contract()
    test_render = '''\npragma solidity ^0.4.11;\n\ncontract Something {\n    string public constant symbol = "TST";\n    string public constant asset_name = "TEST";\n    uint8 public constant decimals = 18;\n    uint256 _totalSupply = 100000000000000000000000;\n\n '''
    tr = c.generate_new_contract(payload)
    assert test_render in tr


