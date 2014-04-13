import sqlite3

with sqlite3.connect('russia.db') as connection:
    c = connection.cursor()
    table_create_query = '''CREATE TABLE IF NOT EXISTS kremlin 
                            (id INTEGER PRIMARY KEY, title TEXT, 
                            body TEXT, keywords TEXT, 
                            post_date DATE, link TEXT) '''
    c.execute(table_create_query)
    c.execute('SELECT * FROM kremlin2')
    rows = c.fetchall()
    for r in rows:
        c.execute(\
            'INSERT INTO kremlin (title, body, keywords, post_date, link) '
            'VALUES (?, ?, ?, ?, ?)',
            (r[0], r[1], r[2], r[3], r[4])
            )

