import sys
import logging
import os
import re

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

DATA_FOLTER = "data"
SPECS_FOLDER = "specs"
SPECS_FORMAT = re.compile(r"^[a-zA-Z0-9]+$")
DATAFILE_FORMAT = re.compile(r"^[a-zA-Z0-9]+_\d{4}-\d{2}-\d{2}\.txt$")

PROJECT_PATH = os.path.dirname(__file__)
DB_PATH = PROJECT_PATH
DB_ENGINE = "sqlite"
DB_NAME = "PARSE_FILE.db"

APP_PORT = 5000
APP_HOST = "0.0.0.0"

# test
TEST_DB_PATH = PROJECT_PATH
TEST_DB_ENGINE = "sqlite"
TEST_DB_NAME = "TEST_PARSE_FILE.db"
