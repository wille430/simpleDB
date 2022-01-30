from pydoc import doc
from numpy import random
import unittest
from simpleDB.db import Database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.table_name = 'users'

        cols = {
            'username': str,
            'password': str,
            'age': int,
            'isCool': bool
        }

        self.db.create_table(self.table_name, cols)

        # populate database
        docs_count = 20
        for i in range(0, docs_count):
            self.db.table(self.table_name).insert({
                'username': '123',
                'password': '123',
                'age': 1,
                'isCool': False
            })

    def tearDown(self):
        # clear db
        self.db.clear()

    def test_insert(self):
        value = {
            'username': '123',
            'password': '123'
        }

        # insert row
        row_id = self.db.table(self.table_name).insert(value)

        self.assertEqual(self.db.table(self.table_name).find(row_id), value)

    def test_find(self):
        value = {
            'username': '123',
            'password': '123'
        }

        # insert row
        row_id = self.db.table(self.table_name).insert(value)

        found_doc = self.db.table(self.table_name).find(row_id)

        self.assertEqual(found_doc, value)

    def test_delete(self):
        # get all keys in dict
        keys = list(self.db.table(self.table_name).rows().keys())

        # get random key
        key = keys[random.randint(len(keys)-1)]

        print(f'Deleting users/{key}')
        self.db.table(self.table_name).delete(f'users/{key}')

        # expect to be none
        self.assertEqual(self.db.table(self.table_name).find(f'users/{key}'), None)

    def test_clear(self):
        self.db.clear()


if __name__ == '__main__':
    unittest.main()
