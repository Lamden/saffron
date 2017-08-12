import os

WORKING_DIR = '../test_project'
cdir = os.path.dirname(__file__)
WORKING_DIR = os.path.abspath(os.path.join(cdir, WORKING_DIR))
DB_FILE = os.path.abspath(os.path.join(WORKING_DIR, 'directory.db'))
try:
    open(DB_FILE,'w').close()
    os.mkdir(WORKING_DIR)
except:
    pass