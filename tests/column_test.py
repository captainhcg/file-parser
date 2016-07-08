import unittest

from column import make_column_type
from column import TextColumn
from column import BooleanColumn
from column import IntegerColumn


class ColumnTestCase(unittest.TestCase):
    def test_make_column_type(self):
        self.assertIsInstance(make_column_type("TEXT", "foo", 1), TextColumn)
        self.assertIsInstance(make_column_type("INTEGER", "foo", 1), IntegerColumn)
        self.assertIsInstance(make_column_type("BOOLEAN", "foo", 1), BooleanColumn)


class TextColumnTestCase(unittest.TestCase):
    def test_formatted_width(self):
        self.assertEqual(TextColumn("foo", 5).formatted_width, 5)
        self.assertEqual(TextColumn("foobar", 5).formatted_width, 6)

    def test_formatted_column_name(self):
        self.assertEqual(TextColumn("foo", 5).formatted_column_name, "foo  ")
        self.assertEqual(TextColumn("foobar", 5).formatted_column_name, "foobar")

    def test_get_formatted_value(self):
        column = TextColumn("foo", 5)
        self.assertEqual(column.get_formatted_value("bar"), "bar  ")

    def test_get_db_value(self):
        column = TextColumn("foo", 5)
        self.assertEqual(column.get_db_value(" bar "), " bar ")


class BooleanColumnTestCase(unittest.TestCase):
    def test_formatted_width(self):
        self.assertEqual(BooleanColumn("foo", 6).formatted_width, 6)
        self.assertEqual(BooleanColumn("foobar", 5).formatted_width, 6)
        self.assertEqual(BooleanColumn("foo", 3).formatted_width, 5)

    def test_formatted_column_name(self):
        self.assertEqual(BooleanColumn("foo", 5).formatted_column_name, "foo  ")
        self.assertEqual(BooleanColumn("foobar", 5).formatted_column_name, "foobar")

    def test_get_formatted_value(self):
        column = BooleanColumn("foo", 5)
        self.assertEqual(column.get_formatted_value(1), "True ")
        self.assertEqual(column.get_formatted_value(0), "False")

    def test_get_db_value(self):
        column = BooleanColumn("foo", 5)
        self.assertEqual(column.get_db_value("1"), 1)
        self.assertEqual(column.get_db_value(" 0"), 0)


class IntegerColumnTestCase(unittest.TestCase):
    def test_formatted_width(self):
        self.assertEqual(IntegerColumn("foo", 6).formatted_width, 6)
        self.assertEqual(IntegerColumn("foobar", 5).formatted_width, 6)

    def test_formatted_column_name(self):
        self.assertEqual(IntegerColumn("foo", 5).formatted_column_name, "foo  ")
        self.assertEqual(IntegerColumn("foobar", 5).formatted_column_name, "foobar")

    def test_get_formatted_value(self):
        column = IntegerColumn("foo", 5)
        self.assertEqual(column.get_formatted_value(1), "    1")
        self.assertEqual(column.get_formatted_value(-1), "   -1")
        self.assertEqual(column.get_formatted_value(0), "    0")
        self.assertEqual(column.get_formatted_value(12345), "12345")

    def test_get_db_value(self):
        column = IntegerColumn("foo", 5)
        self.assertEqual(column.get_db_value("1"), 1)
        self.assertEqual(column.get_db_value("-1"), -1)
        self.assertEqual(column.get_db_value("0"), 0)
        self.assertEqual(column.get_db_value("12345"), 12345)
