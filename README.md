
# Saffron
#### Better Blockchains for Real World Applications

![Travis CI](https://travis-ci.org/Lamden/saffron.svg?branch=master)
![Travis CI](https://readthedocs.org/projects/saffron/badge/?version=latest)


Saffron is a project that aims to make construction and deployment of blockchains easy for developers and enterprises. In it's current form, it relies on the Ethereum technology as a solid base to serve a blockchain with a ton of great features for most use-cases. Here are our goals:

 * Create a Blockchain CLI generator for easy initialization, management, and deployment of private blockchains.
 * Remove transaction costs for using private chains for higher incentive of integration.
 * Provide API's and tools to integrate private chains into web and mobile applications.
 * Create private chain to private chain communication via a main chain 'router' that is free to transact upon.

#### Where are we at so far?
Right now, we have a simple MVP, which generates contracts for Ethereum blockchains and an API that treats smart contract interaction like API calls. As well as a suite of opensource and optionally deployable admin dashboards.

## Give it a go

```
virtualenv -p python3 venv3_saffron
source venv_saffron/bin/activate
python3 setup.py develop

mkdir saffron
export LAMDEN_HOME=$(pwd)/saffron
export LAMDEN_FOLDER_PATH=$(pwd)
export LAMDEN_DB_FILE=$(pwd)/saffron/saffron.db

saffron --help
```

## API Deployment

### deploying the developer services

```
# Install docker for your platform, and then.
docker-compose up
```

#### You can try out the API by using the following bash commands:

Simple version:
```
cd docker_saffron_ledger_api && gunicorn api:application
echo 'pragma solidity ^0.4.11;contract mortal { address owner; function mortal() { owner = msg.sender; } function kill() { if (msg.sender == owner) suicide(owner); } } contract greeter is mortal { string greeting; function greeter(string _greeting) public { greeting = _greeting; } function greet() constant returns (string) { return greeting; } }' | curl --data-binary @- localhost:8000/some_endpoint
```

Example:
```
$ echo 'pragma solidity ^0.4.11;contract mortal { address owner; function mortal() { owner = msg.sender; } function kill() { if (msg.sender == owner) suicide(owner); } } contract greeter is mortal { string greeting; function greeter(string _greeting) public { greeting = _greeting; } function greet() constant returns (string) { return greeting; } }' | curl --data-binary @- localhost:8000/some_endpoint
Created the following files:
    ['greeter.abi', 'greeter.bin', 'mortal.abi', 'mortal.bin']
```

#### running the tests

```
virtualenv venv_saffron
source venv_saffron/bin/activate
python setup.py develop
pip install pytest
py.tests tests
```

## Documentation

 - http://saffron.readthedocs.io/en/latest/
