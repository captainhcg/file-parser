import unittest
import app as parse_app
import settings

from mock import patch
from flask.ext.testing import TestCase
from sqlalchemy import Table, Column, Integer, String, text

from models import db
from models import Specification

from column import ColumnBase
from column import TextColumn
from column import BooleanColumn
from column import IntegerColumn

from specification import get_header_output
from specification import get_row_output
from specification import get_spec_path
from specification import get_table_name_by_spec_name
from specification import import_specification
from specification import import_specification_by_name
from specification import is_specification_imported
from specification import load_columns_from_spec_file
from specification import load_table_from_specification
from specification import make_column
from specification import make_column_dict

import os

TEST_SPEC_NAME = "test"
TEST_SPEC_PATH = "tests/test.csv"

class SpecDBTestBase(TestCase):
    def create_app(self):
        app = parse_app.app
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + settings.TEST_DB_NAME
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.unlink(settings.TEST_DB_NAME)  # dirty hack to clean up test.db


class SpecTestCase(SpecDBTestBase):
    def test_is_specification_imported(self):
        self.assertEqual(is_specification_imported(TEST_SPEC_NAME), False)

        spec = Specification(specification_name=TEST_SPEC_NAME)
        db.session.add(spec)
        db.session.commit()
        self.assertEqual(is_specification_imported(TEST_SPEC_NAME), False)
        create_test_table()
        self.assertEqual(is_specification_imported(TEST_SPEC_NAME), True)

    def test_import_specification(self):
        with open(TEST_SPEC_PATH) as f:
            import_specification(TEST_SPEC_NAME, f)
        self.assertEqual(is_specification_imported(TEST_SPEC_NAME), True)

    @patch("specification.is_specification_imported")
    @patch("specification.get_spec_path")
    def test_load_table_from_specification(self, mock_get_path, mock_is_imported):
        mock_is_imported.return_value = False
        with self.assertRaises(Exception):
            load_table_from_specification(TEST_SPEC_NAME)

        mock_get_path.return_value = TEST_SPEC_PATH
        mock_is_imported.return_value = True
        with open(TEST_SPEC_PATH) as f:
            import_specification(TEST_SPEC_NAME, f)

        table, _ =\
            load_table_from_specification(TEST_SPEC_NAME)
        self.assertIsInstance(table, Table)


def create_test_table():
    query = text("""
        CREATE TABLE spec_test (
        name VARCHAR,
        valid INTEGER,
        count INTEGER
    );""")
    db.engine.execute(query)
    db.session.commit()


def get_sample_column_objects_list():
    return [
        TextColumn("name", 10),
        BooleanColumn("valid", 1),
        IntegerColumn("count", 3),
    ]

class SpecUtilTestCase(unittest.TestCase):

    def test_get_spec_path(self):
        self.assertEqual(get_spec_path(TEST_SPEC_NAME), '/specs/test.csv')

    def test_load_columns_from_spec_file(self):
        with open(TEST_SPEC_PATH) as f:
            columns, column_objects_list = load_columns_from_spec_file(f)
        self.assertEqual(len(columns), 3)
        self.assertEqual(
            all([isinstance(c, Column) for c in columns]), True)
        self.assertEqual(len(column_objects_list), 3)
        self.assertEqual(
            all([isinstance(c, ColumnBase) for c in column_objects_list]), True)

    @patch("specification.import_specification")
    @patch("specification.get_spec_path")
    @patch("specification.is_specification_imported")
    def test_import_specification_by_name(
            self, mock_is_imported, mock_get_path, mock_import_spec):
        mock_is_imported.return_value = True
        with self.assertRaises(Exception):  # already imported, raise error
            import_specification_by_name(TEST_SPEC_NAME)

        mock_is_imported.return_value = False
        mock_get_path.return_value = TEST_SPEC_PATH
        import_specification_by_name(TEST_SPEC_NAME)
        mock_import_spec.assert_called_once()

    def test_get_table_name_by_spec_name(self):
        self.assertEqual(
            get_table_name_by_spec_name("123abd"), "spec_123abd")
        with self.assertRaises(ValueError):
            get_table_name_by_spec_name("123_abd")

    def test_make_column_dict(self):
        columns_rows = ["column name", "width", "datatype"]
        self.assertDictEqual(
            make_column_dict(columns_rows), {'C': 0, 'D': 2, 'W': 1})

    def test_make_column(self):
        column_dict = {'C': 0, 'D': 2, 'W': 1}
        column_schema, column_type = make_column(["foo", "10", "TEXT"], column_dict)
        self.assertEqual(column_schema.name, "foo")
        self.assertIsInstance(column_schema.type, String)
        self.assertIsInstance(column_type, TextColumn)

        column_schema, column_type = make_column(["bar", "10", "BOOLEAN"], column_dict)
        self.assertIsInstance(column_schema.type, Integer)
        self.assertIsInstance(column_type, BooleanColumn)

        column_schema, column_type = make_column(["bar", "10", "INTEGER"], column_dict)
        self.assertIsInstance(column_schema.type, Integer)
        self.assertIsInstance(column_type, IntegerColumn)

    def test_get_header_output(self):
        column_objects_list = get_sample_column_objects_list()
        line1, line2 = get_header_output(column_objects_list)
        self.assertEqual(line1, "name      |valid|count")
        self.assertEqual(line2, "----------|-----|-----")

    def test_get_row_output(self):
        column_objects_list = get_sample_column_objects_list()
        row = (u'Quuxitude', 1, 103)
        self.assertEqual(
            get_row_output(column_objects_list, row), "Quuxitude |True |  103")
