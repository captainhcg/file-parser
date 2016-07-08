# -*- coding: utf-8 -*-
import csv
from sqlalchemy import Table, Column, Integer, String, MetaData, text

from settings import logging
from settings import PROJECT_PATH
from settings import SPECS_FOLDER
from settings import SPECS_FORMAT
from app import db

from column import make_column_type
from models import Specification

logger = logging.getLogger(__name__)

TABLE_SPLITTER = "|"


def get_spec_path(spec_name):
    return PROJECT_PATH + '/' + SPECS_FOLDER + '/' + spec_name + ".csv"


def get_table_name_by_spec_name(spec_name):
    """
    Get table name by specificaiton name, also validate the format of specificaiton name
    """
    if not SPECS_FORMAT.match(spec_name):
        raise ValueError("Invalid spec_name %s", spec_name)
    return u"spec_%s" % spec_name


def import_specification_by_name(spec_name):
    """
    Given a specificaiton name, attempt to locate the csv file in spec folder
    and create a table dynamically
    """
    if is_specification_imported(spec_name):
        raise Exception(
            "Specification [%s] has been imported already" % spec_name)

    path = get_spec_path(spec_name)
    with open(path, "r") as spec_file:
        import_specification(spec_name, spec_file)


def is_specification_imported(spec_name):
    """
    TODO: Check if the specification has been imported already we should
    perform 2 checks:
    1. If the spec_name in Specification?
    2. If a table with spec_name has been created
    """
    kwargs = {
        'specification_name': spec_name,
    }
    row = db.session.query(Specification).filter_by(**kwargs).first()
    if not row:
        return False
    query = text("SELECT name FROM sqlite_master WHERE type='table' AND name='spec_%s';" % spec_name)
    result = db.engine.execute(query).fetchall()
    if result:
        return True
    else:
        return False


def make_column(row, column_dict):
    """
    name,10,TEXT
    valid,1,BOOLEAN
    count,3,INTEGER
    """
    column_name_idx = column_dict["C"]
    column_width_idx = column_dict["W"]
    column_datatype_idx = column_dict["D"]

    column_datatype_map = {
        "TEXT": String,
        "BOOLEAN": Integer,
        "INTEGER": Integer,
    }
    column_name = row[column_name_idx]
    column_width = int(row[column_width_idx])  # width is not being used
    column_datatype = column_datatype_map[row[column_datatype_idx]]

    column_type = make_column_type(
        row[column_datatype_idx], column_name, column_width)

    return Column(column_name, column_datatype), column_type


def make_column_dict(columns_rows):
    """
    input:
    ["column name", "width", "datatype"]

    output:
    {'C': 0, 'D': 2, 'W': 1}
    """
    column_dict = {}
    for idx, column in enumerate(columns_rows):
        if column == "column name":
            column_dict["C"] = idx
        elif column == "width":
            column_dict["W"] = idx
        elif column == "datatype":
            column_dict["D"] = idx
    return column_dict


def load_columns_from_spec_file(spec_file):
    """
    Return a list of Columns and a dict of make_column_dict()

    Use Columns list as column_object of Table; Use dict to for convinence
    """
    columns = []
    column_dict = {}
    column_objects_list = []
    for idx, row in enumerate(csv.reader(spec_file, dialect=csv.excel)):
        if idx == 0:
            column_dict = make_column_dict(row)
        else:
            try:
                column, column_object = make_column(row, column_dict)
                columns.append(column)
                column_objects_list.append(column_object)
            except Exception as e:
                logger.exception(e)
                raise ValueError("Invalid Column definition: %s", row)
    return columns, column_objects_list


def import_specification(spec_name, spec_file):
    """
    Here we dynamically create table and then insert a Specification record
    """
    columns, _ = load_columns_from_spec_file(spec_file)
    metadata = MetaData(bind=db.engine)
    table_name = get_table_name_by_spec_name(spec_name)
    specific_table = Table(table_name, metadata, *columns)
    metadata.create_all(tables=[specific_table])

    spec = Specification(
        specification_name=spec_name,
    )
    db.session.add(spec)
    db.session.commit()


def load_table_from_specification(spec_name):
    if not is_specification_imported(spec_name):
        raise Exception(
            "Specification [%s] has not been imported yet!", spec_name)

    path = get_spec_path(spec_name)
    with open(path, "r") as spec_file:
        columns, column_objects_list = load_columns_from_spec_file(spec_file)
        metadata = MetaData(bind=db.engine)
        table_name = get_table_name_by_spec_name(spec_name)
        return Table(table_name, metadata, *columns), column_objects_list


def get_header_output(column_objects_list):
    header_list = []
    split_line = []

    for column in column_objects_list:
        header_list.append(column.formatted_column_name)
        split_line.append("-" * column.formatted_width)

    return [
        TABLE_SPLITTER.join(header_list),
        TABLE_SPLITTER.join(split_line),
    ]


def get_row_output(column_objects_list, row):
    fields = []
    for column, value in zip(column_objects_list, row):
        fields.append(column.get_formatted_value(value))
    return TABLE_SPLITTER.join(fields)


def select_all_from_specification(spec_name):
    specification_table, column_objects_list =\
        load_table_from_specification(spec_name)
    specification_table.select().execute().fetchall()
    for line in get_header_output(column_objects_list):
        print(line)
    for row in specification_table.select().execute().fetchall():
        print(get_row_output(column_objects_list, row))
