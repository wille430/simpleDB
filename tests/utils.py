from simpleDB.db import Database


def populate_database(db: Database, table_name='test_table'):
    """Populate a database with mock data.

    :param db: An instance of ``Database``
    :param table_name: The name of the table to add mock data
    :return: Database with data added
    """

    cols = {
        'username': str,
        'password': str,
        'age': int,
        'isCool': bool
    }

    db.create_table(table_name, cols)

    # populate database
    docs_count = 20
    for i in range(0, docs_count):
        db.table(table_name).insert({
            'username': '123',
            'password': '123',
            'age': 1,
            'isCool': False
        })

    return db
