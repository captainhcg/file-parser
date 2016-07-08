import unittest
from mock import patch
from models import db

from sqlalchemy import text

from importer import get_data_file_path
from importer import get_row_dict
from importer import import_data_files
from importer import import_data_file
from specification_test import create_test_table
from specification_test import get_sample_column_objects_list
from specification_test import SpecDBTestBase
from specification_test import TEST_SPEC_PATH

TEST_DATA_FILE_NAME = "tests/datafiles/test_2007-10-01.txt"
TEST_DATA_FILE_PATH = "tests/datafiles/"


class ImporterUtilTestCase(unittest.TestCase):
    def test_get_spec_path(self):
        self.assertEqual(get_data_file_path(), '/data/')

    @patch("importer.import_data_file")
    @patch("importer.get_data_file_path")
    @patch("importer.is_specification_imported")
    def test_import_data_files(
            self, mock_is_imported, mock_get_path, mock_import_data_file):
        mock_get_path.return_value = TEST_DATA_FILE_PATH
        mock_is_imported.return_value = True
        import_data_files()
        self.assertEqual(mock_import_data_file.call_count, 2)

    def test_get_row_dict(self):
        schema = get_sample_column_objects_list()
        line = "Foony     1  1\n"
        self.assertDictEqual(
            get_row_dict(schema, line),
            {'count': 1, 'valid': 1, 'name': u'Foony'}
        )

class ImporterTestCase(SpecDBTestBase):
    @patch("specification.is_specification_imported")
    @patch("specification.get_spec_path")
    def test_import_data_file(self, mock_get_path, mock_is_imported):
        mock_is_imported.return_value = True
        mock_get_path.return_value = TEST_SPEC_PATH
        create_test_table()
        import_data_file(TEST_DATA_FILE_NAME)
        query = text("select * from spec_test")
        res = db.engine.execute(query).fetchall()
        self.assertEqual(len(res), 3)
