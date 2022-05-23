import os
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
        try:
            self.db.clear()
            self.db.save_and_close()
        except:
            return

    def test_clear(self):
        self.db.clear()

        # expect all tables to be removed
        self.assertEqual(self.db.tables(), {})

    # def test_consistent_storage(self):
    #     self.maxDiff = None
    #     self.db = populate_database(self.db, self.table_name)

    #     print('Reading decrypted data...')
    #     decrypted_data = self.db.table(self.table_name)

    #     self.db.save_and_close()

    #     print('Reopening encrypted database')
    #     self.db = Database()

    #     self.assertEqual(self.db.table(self.table_name).serialize(),
    #                      decrypted_data.serialize())

    #     self.db.save_and_close()

    #     self.assertFalse(os.path.exists(self.db.storage.temp_path))

    def test_encryption(self):
        self.db = populate_database(self.db, self.table_name)

        raw_data = self.db.storage.read()
        self.db.save()

        with open(self.db.storage.out_path, 'rb') as f:
            self.assertNotEqual(raw_data, f.read())


if __name__ == '__main__':
    unittest.main()
