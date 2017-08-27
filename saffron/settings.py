import os, configparser
from os.path import join
run_location, filename = os.path.split(os.path.abspath(__file__))
config = configparser.ConfigParser()

config.read(os.path.join(run_location, 'config/default.conf'))
lamden_home = os.environ.get('LAMDEN_HOME', None) if os.environ.get('LAMDEN_HOME', None) else os.path.expanduser(config.defaults()['lamden_home']) # ~/.lamden
lamden_folder_path = os.environ.get('LAMDEN_FOLDER_PATH', None) if os.environ.get('LAMDEN_FOLDER_PATH', None) else join(lamden_home, config.defaults()['lamden_folder_path']) # ~/.lamden/lamden-default
lamden_db_file = os.environ.get('LAMDEN_DB_FILE', None) if os.environ.get('LAMDEN_DB_FILE', None) else join(lamden_folder_path, config.defaults()['lamden_db_file']) # ~/

PASSWORD_FILE_NAME = '.pass'
PROCESS_FILE_NAME = '.pid'
GENESIS_FILE_NAME = 'genesis.json'

try:
    os.makedirs(lamden_folder_path)
except OSError as e:
    pass