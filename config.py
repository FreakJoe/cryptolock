import os
import sys

DATA_DIR_NAME = 'data'
DB_NAME = 'documents'
TEST_DB_NAME = 'test'

# Determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
elif __file__:
    BASE_PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_PATH, DATA_DIR_NAME)