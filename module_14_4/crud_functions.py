import sqlite3


def initiate_db():
    connection = sqlite3.connect('products.dp')
    cursor = connection.cursor()

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Products(
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT,
                        price TEXT NOT NULL)
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
    connection.close()


def get_all_products():
    connection = sqlite3.connect('products.dp')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products
