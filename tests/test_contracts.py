# from reconf.location import TestStringLocation as TSL
# from bowie import config
# from bowie.download import proxies
import pytest
import re, json
from hadronutils import contracts
from tempfile import NamedTemporaryFile as ntf
import uuid

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
            return true;
        } else {
            return false;
        }
    }

    function approve(address _spender, uint256 _amount) returns (bool success) {
        allowed[msg.sender][_spender] = _amount;
        return true;
    }
 
    function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }
}
'''

payload = {'asset_name': 'TEST',
    'contract_name': 'Something',
    'solidity_version': '^0.4.11',
    'decimals': 18,
    'symbol': 'TST',
    '_totalSupply': 100000000000000000000000,
    'sol': sol_contract}

def test_contracts():
    new_contract = str(uuid.uuid1())
    with ntf() as t:
        c_name, rendered = contracts.render_contract(payload.copy())
        t.write(rendered.encode('utf8'))
        t.seek(0)
        c = Contract(new_contract, t.name)
        assert hasattr(c, 'abi')
        assert hasattr(c, 'address')
        assert hasattr(c, 'bytecode')
        assert hasattr(c, 'compiled_name')
        assert hasattr(c, 'contracts')
        assert hasattr(c, 'deploy')
        assert hasattr(c, 'from_chain')
        assert hasattr(c, 'gas_estimate')
        assert hasattr(c, 'instance')
        assert hasattr(c, 'is_deployed')
        assert hasattr(c, 'metadata')
        assert hasattr(c, 'method_identifiers')
        assert hasattr(c, 'name')
        assert hasattr(c, 'output_json')
        assert hasattr(c, 'sol')
        assert hasattr(c, 'template_json')
        assert c.__dict__['name'] == new_contract
        assert c.__dict__['gas_estimate'] == {u'creation': {u'executionCost': u'20627', u'totalCost': u'611627', u'codeDepositCost': u'591000'}, u'external': {u'approve(address,uint256)': u'20468', u'symbol()': u'694', u'balanceOf(address)': u'637', u'totalSupply()': u'414', u'FixedSupplyToken()': u'41108', u'owner()': u'563', u'allowance(address,address)': u'869', u'asset_name()': u'628', u'transfer(address,uint256)': u'42094', u'transferFrom(address,address,uint256)': u'62799', u'decimals()': u'261'}}


