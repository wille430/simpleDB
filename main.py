from simpleDB.db import Database


def main():
    db = Database('database.db')

    db.set({
        'username': 'wille430'
    }, 'users/1')

    db.append({
        'username': 'test123'
    }, 'users')

    db.save()


if __name__ == '__main__':
    main()
