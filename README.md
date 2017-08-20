# Hadron Ledger
#### Better Blockchains for Real World Applications

![Travis CI](https://travis-ci.org/Hadron-Ledger/hadron.svg?branch=master)

Hadron is a project that aims to make construction and deployment of blockchains easy for developers and enterprises. In it's current form, it relies on the Ethereum technology as a solid base to serve a blockchain with a ton of great features for most use-cases. Here are our goals:

 * Create a Blockchain CLI generator for easy initialization, management, and deployment of private blockchains.
 * Remove transaction costs for using private chains for higher incentive of integration.
 * Provide API's and tools to integrate private chains into web and mobile applications.
 * Create private chain to private chain communication via a main chain 'router' that is free to transact upon.

#### Where are we at so far?
Right now, we have an extremely rudementary generator for Ethereum blockchains and an API that treats smart contract interaction like API calls.

## Give it a go

```
virtualenv venv_hadron
source venv_hadron/bin/activate
python setup.py develop
```

## API Deployment
#### You can try out the API by using the following bash commands:

Simple version:
```
cd docker_hadron_ledger_api && gunicorn api:application
echo 'pragma solidity ^0.4.11;contract mortal { address owner; function mortal() { owner = msg.sender; } function kill() { if (msg.sender == owner) suicide(owner); } } contract greeter is mortal { string greeting; function greeter(string _greeting) public { greeting = _greeting; } function greet() constant returns (string) { return greeting; } }' | curl --data-binary @- localhost:8000/some_endpoint
```

Advanced version:
```
docker pull ethereum/client-go
docker build -t hadron-ledger-api docker_hadron_ledger_api
docker-compose up
```

Example:
```
$ echo 'pragma solidity ^0.4.11;contract mortal { address owner; function mortal() { owner = msg.sender; } function kill() { if (msg.sender == owner) suicide(owner); } } contract greeter is mortal { string greeting; function greeter(string _greeting) public { greeting = _greeting; } function greet() constant returns (string) { return greeting; } }' | curl --data-binary @- localhost:8000/some_endpoint
Created the following files:
    ['greeter.abi', 'greeter.bin', 'mortal.abi', 'mortal.bin']
```

#### running the tests

```
virtualenv venv_hadron
source venv_hadron/bin/activate
python setup.py develop
pip install pytest
py.tests tests
```