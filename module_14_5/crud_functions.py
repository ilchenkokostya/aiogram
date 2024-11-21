import sqlite3

connection = sqlite3.connect('products.dp')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Products(
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT,
                        price TEXT NOT NULL)
    ''')

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Users(
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        balance INTEGER NOT NULL)
    ''')

    cursor.execute('DELETE FROM Products')

    description = (
        'Доппельгерц актив',
        'Турбослим Альфа',
        'Глицин форте вишня',
        'Грин Слим'
    )
    for i in range(1, 5):
        cursor.execute(
            'INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
            (f'{i}', f'{description[i - 1]}', f'{i * 100}')
        )
    connection.commit()
    # connection.close()


def add_user(username, email, age):
    cursor.execute(f"INSERT INTO Users (username, email, age, balance) VALUES ('{username}', '{email}', '{age}', 1000)")
    connection.commit()
    # connection.close()


def is_included(username):
    user = cursor.execute(f"SELECT * FROM Users WHERE lower(username) = lower(?)", (username,))
    connection.commit()
    # connection.close()
    return True if user.fetchone() is None else False


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    # connection.close()
    return products
