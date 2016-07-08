# -*- coding: utf-8 -*-
import glob
import os
import codecs

from settings import logging
from settings import PROJECT_PATH
from settings import DATA_FOLTER
from settings import DATAFILE_FORMAT
from app import db

from specification import is_specification_imported
from specification import load_table_from_specification

logger = logging.getLogger(__name__)


def get_data_file_path():
    return PROJECT_PATH + '/' + DATA_FOLTER + '/'


def import_data_files():
    path = get_data_file_path()
    for data_file in glob.glob(path + "*.txt"):
        _, fname = os.path.split(data_file)
        if not DATAFILE_FORMAT.match(fname):
            continue

        spec_name = fname.split("_", 1)[0]
        if not is_specification_imported(spec_name):
            raise Exception(
                "Specification [%s] has not been imported yet" % spec_name)

        import_data_file(data_file)


def get_row_dict(schema, line):
    row_dict = {}
    start_idx = 0
    for column in schema:
        width = column.width
        raw_data = line[start_idx: start_idx + width].strip()
        start_idx += width
        row_dict[column.name] = column.get_db_value(raw_data)
    return row_dict


def import_data_file(data_file):
    _, fname = os.path.split(data_file)
    spec_name = fname.split("_", 1)[0]
    # logger.info("Import data file [%s] start", fname)
    specification_table, schema =\
        load_table_from_specification(spec_name)
    con = db.engine.connect()
    with codecs.open(data_file, "r", "utf-8") as f:
        for line in f:
            row_dict = get_row_dict(schema, line)
            con.execute(specification_table.insert(), **row_dict)
    # logger.info("Import data file [%s] end", fname)
