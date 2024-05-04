#Для создания двух баз данных SQLite с положительными и отрицательными привычками,
import sqlite3

def create_connection(db_file):
    """ Создание соединения с SQLite базой данных """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"SQLite connection is established: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ Создание таблицы с использованием предоставленного SQL запроса """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def show_table(conn):
    """ Вывод содержимого таблицы """
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM habits")
        rows = c.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)

def main():
    database_positive = "positive_habits1.db"
    database_negative = "negative_habits1.db"

    sql_create_habits_table = """
    CREATE TABLE IF NOT EXISTS habits (
        id integer PRIMARY KEY,
        habit text NOT NULL UNIQUE
    );
    """

    # Создание баз данных и таблиц
    conn_positive = create_connection(database_positive)
    conn_negative = create_connection(database_negative)

    if conn_positive:
        create_table(conn_positive, sql_create_habits_table)
        try:
            conn_positive.executemany("INSERT INTO habits (habit) VALUES (?)", [
                ("Ранний подъем",), ("Регулярные физические упражнения",),
                ("Достаточный сон",), ("Здоровое питание",), ("Благодарность",)])
            conn_positive.commit()
        except sqlite3.IntegrityError:
            print("Attempt to insert duplicate data in positive_habits.db")
        show_table(conn_positive)
        conn_positive.close()

    if conn_negative:
        create_table(conn_negative, sql_create_habits_table)
        try:
            conn_negative.executemany("INSERT INTO habits (habit) VALUES (?)", [
                ("Курение",), ("Недосыпание",),
                ("Переедание",), ("Злоупотребление сладким",), ("Чрезмерное использование гаджетов",)])
            conn_negative.commit()
        except sqlite3.IntegrityError:
            print("Attempt to insert duplicate data in negative_habits.db")
        show_table(conn_negative)
        conn_negative.close()

    print("Databases have been created and populated successfully.")

if __name__ == '__main__':
    main()


