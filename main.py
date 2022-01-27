from simpleDB.Table import Table
from simpleDB.db import Database


def main():
    db = Database('database.db')

    cols = {
        'username': str,
        'password': str,
        'age': int
    }
    new_table = Table('users', cols) 
    db.create_table(new_table)

    db.save()


if __name__ == '__main__':
    main()
