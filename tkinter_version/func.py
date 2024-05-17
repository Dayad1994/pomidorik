import datetime
import sqlite3


def seconds_to_ftime(seconds):
    '''seconds to formatting time'''
    m = str(seconds // 60).rjust(2, "0")
    s = str(seconds % 60).rjust(2, "0")
    ftime = f'{m}:{s}'
    return ftime


def create_db():
    '''создание базы данных и таблицы'''
    try:
        conn = sqlite3.connect('sqlite_python.db')
        cursor = conn.cursor()
        print('Подключен к SQLite')

        query = '''create table pomodoro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_time date);'''
        cursor.execute(query)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print('Ошибка при подключении к sqlite', error)
    finally:
        if conn:
            conn.close()
            print('Соединение с SQLite закрыто')


def write_db():
    '''запись помидоро в таблицу'''
    try:
        conn = sqlite3.connect('sqlite_python.db',
                               detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        print('Подключен к SQLite для записи')

        curdate = (datetime.date.today(),)
        query = '''insert into pomodoro ('data_time')
                values (?);'''
        cursor.execute(query, curdate)
        conn.commit()
        query_count = '''select count(*) from pomodoro'''
        cursor.execute(query_count)
        count = cursor.fetchone()
        cursor.close()
        return count[0]
    except sqlite3.Error as error:
        print('Ошибка при подключении к sqlite', error)
    finally:
        if conn:
            conn.close()
            print('Соединение с SQLite закрыто')


def read_db():
    '''чтение строк с таблицы. возвращает список строк в виде кортежей'''
    try:
        conn = sqlite3.connect('sqlite_python.db')
        cursor = conn.cursor()
        print('Подключен к SQLite для чтения')

        query = '''select * from pomodoro'''
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except sqlite3.Error as error:
        print('Ошибка при подключении к sqlite', error)
    finally:
        if conn:
            conn.close()
            print('Соединение с SQLite закрыто')


def today_pomodoro():
    '''возвращает кол-во помидоров за текущий день'''
    records = read_db()
    today = str(datetime.date.today())
    count = 0
    for row in records:
        if today == row[1]:
            count += 1
    return count
