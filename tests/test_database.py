import unittest
from simpleDB.db import Database
from tests.utils import populate_database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.table_name = 'users'

        self.db = populate_database(self.db)

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
