from pydoc import doc
from numpy import random
import unittest
from simpleDB.db import Database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database('test_db.db')

        docs_count = 20
        for i in range(0, docs_count):
            value = dict(list(enumerate([0]*16)))
            self.db.append('users', value)

    def tearDown(self):
        # clear db
        self.db.clear()

    def test_set(self):
        path = 'users/1'
        value = {
            'username': '123',
            'password': '123'
        }

        # set doc
        self.db.set(path, value)

        self.assertEqual(self.db.find(path), value)

    def test_find(self):
        new_doc = self.db.set('users/1', {'username': '123'})
        found_doc = self.db.find('users/1')

        self.assertEqual(found_doc, new_doc)

    def test_append(self):
        value = {
            '123': '123'
        }
        path = 'users'

        new_path, new_value = self.db.append(path, value)

        self.assertIn(path, new_path)
        self.assertEqual(value, new_value)

    def test_delete(self):
        # get all keys in dict
        keys = list(self.db.find('users').keys())

        # get random key
        key = keys[random.randint(len(keys)-1)]

        print(f'Deleting users/{key}')
        self.db.delete(f'users/{key}')

        # expect to be none
        self.assertEqual(self.db.find(f'users/{key}'), None)


if __name__ == '__main__':
    unittest.main()
