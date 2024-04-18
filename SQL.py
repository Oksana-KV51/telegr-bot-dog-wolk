### Шаг 1: Создание базы данных и таблиц
#Сначала создадим базу данных SQLite для хранения данных о привычках.

import sqlite3

conn = sqlite3.connect('habits.db')
c = conn.cursor()
c.execute("SELECT * FROM habits")
#Вводим функцию для выведения информации:
rows = c.fetchall()
for row in rows:
    print(row)
def init_db():
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            habit_name TEXT,
            description TEXT,
            frequency TEXT,
            last_completed DATE
        )
    ''')
    conn.commit()
    conn.close()

init_db()



