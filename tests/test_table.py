import random
import unittest
from simpleDB.db import Database
from tests.utils import populate_database


class TestTable(unittest.TestCase):

    def setUp(self):
        self.table_name = 'users'
        self.db = populate_database(Database(), self.table_name)
        self.table = self.db.table(self.table_name)

    def tearDown(self):
        self.db.clear()
        self.db.close()

    def test_insert(self):
        value = {
            'username': '123',
            'password': '123'
        }

        # insert row
        row_id = self.table.insert(value)

        self.assertEqual(self.table.find(row_id), value)

    def test_find(self):
        value = {
            'username': '123',
            'password': '123'
        }

        # insert row
        row_id = self.table.insert(value)

        found_doc = self.table.find(row_id)

        self.assertEqual(found_doc, value)

    def test_delete(self):
        # get all keys in dict
        keys = list(self.table.rows.keys())

        # get random key
        key = keys[random.randint(0, len(keys)-1)]

        print(f'Deleting users/{key}')
        self.table.delete(f'{key}')

        # expect to be none
        self.assertEqual(self.table.find(f'users/{key}'), None)


if __name__ == '__main__':
    unittest.main()
