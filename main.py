from simpleDB.Table import Table
from simpleDB.db import Database


def main():
    db = Database()

    cols = {
        'username': str,
        'password': str,
        'age': int
    }

    db.create_table('users', cols)
    db.table('users').insert({
        'username': 'test123'
    })


if __name__ == '__main__':
    main()
