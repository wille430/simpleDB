import unittest
from simpleDB.db import Database

class TestDatabase(unittest.TestCase):

    def test_set(self):
        db = Database('test_db.db')
        path = 'users/1'
        value = {
            'username': '123',
            'password': '123'
        }

        # set doc
        db.set(value, path)
        
        self.assertEqual(db.find(path), value)

if __name__ == '__main__':
    unittest.main()