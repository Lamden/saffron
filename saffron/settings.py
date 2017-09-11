import os, configparser
from os.path import join
import subprocess

run_location, filename = os.path.split(os.path.abspath(__file__))
config = configparser.ConfigParser()

config.read(os.path.join(run_location, 'config/default.conf'))
lamden_home = os.environ.get('LAMDEN_HOME', None) if os.environ.get('LAMDEN_HOME', None) else os.path.expanduser(config.defaults()['lamden_home']) # ~/.lamden
lamden_folder_path = os.environ.get('LAMDEN_FOLDER_PATH', None) if os.environ.get('LAMDEN_FOLDER_PATH', None) else join(lamden_home, config.defaults()['lamden_folder_path']) # ~/.lamden/lamden-default
lamden_db_file = os.environ.get('LAMDEN_DB_FILE', None) if os.environ.get('LAMDEN_DB_FILE', None) else join(lamden_folder_path, config.defaults()['lamden_db_file']) # ~/

PASSWORD_FILE_NAME = '.pass'
PROCESS_FILE_NAME = '.pid'
genesis_fn = 'genesis.json'
node_fn = 'node.info'

node_info_json = lambda project_name: os.path.join(os.path.join(lamden_home, project_name), node_fn)
project_genesis = lambda project_name: os.path.join(os.path.join(lamden_home, project_name), genesis_fn)
env_source = lambda project_name: os.path.join(os.path.join(lamden_home, project_name), '{}.source'.format(project_name))

chain_pid = os.path.join(lamden_folder_path, 'chain.pid')

BASH_BIN = subprocess.check_output(['which','bash']).decode('utf-8')
GETH_BIN = subprocess.check_output(['which','geth']).decode('utf-8')

src_string = '''#! /bin/bash
export LAMDEN_HOME='{LAMDEN_HOME}'
export LAMDEN_FOLDER_PATH='{LAMDEN_FOLDER_PATH}'
export LAMDEN_DB_FILE='{LAMDEN_DB_FILE}'
export PROJECT_GENESIS='{PROJECT_GENESIS}'
export NODE_INFO_JSON='{NODE_INFO_JSON}'
'''.format



try:
    os.makedirs(lamden_folder_path)
except OSError as e:
    pass