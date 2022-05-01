import unittest
from simpleDB.Table import Row
from simpleDB.db import Database, Table

from tests.utils import populate_database


class TestQueries(unittest.TestCase):

    def setUp(self):
        self.table_name = 'test_table'
        self.db = populate_database(Database(), self.table_name)
        self.table = self.db.table(self.table_name)

    def tearDown(self):
        self.db.clear()
        self.db.save_and_close()

    def test_equal(self):

        row_data = {
            'username': 'test_find_me',
            'password': '123',
            'age': 1,
            'isCool': False
        }

        # add row
        self.table.insert(Row(row_data))

        result = self.table.query('username', '==', 'test_find_me').first()

        self.assertEqual(row_data, result)

    def test_greater_equal_than(self):

        row_data = {
            'username': 'test_find_me',
            'password': '123',
            'age': 100,
            'isCool': False
        }

        self.table.insert(Row(row_data))

        results = self.table.query('age', '>=', 100)

        for result in results:
            self.assertGreaterEqual(result.setdefault('age'), 100)


    def test_less_equal_than(self):

        row_data = {
            'username': 'test_find_me',
            'password': '123',
            'age': 110,
            'isCool': False
        }

        self.table.insert(Row(row_data))

        results = self.table.query('age', '<=', 100)

        for result in results:
            self.assertLessEqual(result.setdefault('age'), 100)
