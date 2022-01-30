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
        self.db.close()

    def test_clear(self):
        self.db.clear()

        # expect all tables to be removed
        self.assertEqual(self.db.tables(), {})


if __name__ == '__main__':
    unittest.main()
