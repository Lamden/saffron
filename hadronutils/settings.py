import os, configparser
from os.path import join
run_location, filename = os.path.split(os.path.abspath(__file__))
config = configparser.ConfigParser()

config.read(os.path.join(run_location, 'config/default.conf'))
hadron_home = os.environ.get('HADRON_HOME', None) if os.environ.get('HADRON_HOME', None) else os.path.expanduser(config.defaults()['hadron_home']) # ~/.hadron
hadron_folder_path = os.environ.get('HADRON_FOLDER_PATH', None) if os.environ.get('HADRON_FOLDER_PATH', None) else join(hadron_home, config.defaults()['hadron_folder_path']) # ~/.hadron/hadron-default
hadron_db_file = os.environ.get('HADRON_DB_FILE', None) if os.environ.get('HADRON_DB_FILE', None) else join(hadron_folder_path, config.defaults()['hadron_db_file']) # ~/



try:
    os.makedirs(hadron_folder_path)
except OSError as e:
    pass