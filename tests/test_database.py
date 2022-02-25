import unittest
from simpleDB.db import Database
from tests.utils import populate_database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.table_name = 'users'

        self.db = populate_database(self.db, self.table_name)

    def tearDown(self):
        # clear db
        self.db.clear()
        self.db.close()

    def test_clear(self):
        self.db.clear()

        # expect all tables to be removed
        self.assertEqual(self.db.tables(), {})

    def test_encryption(self):
        print('Opening database...')
        self.db = Database(encrypt=True)
        self.db = populate_database(self.db, self.table_name)

        print('Reading decrypted data...')
        decrypted_data = self.db.table(self.table_name)

        self.db.close()

        print('Reopening encrypted database')
        self.db = Database(encrypt=True)

        self.assertEqual(self.db.table(self.table_name), decrypted_data)

        self.db.close()


if __name__ == '__main__':
    unittest.main()
