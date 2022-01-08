import sqlite3
from settings import *


async def write_task(obj, sentry):
    sqlite_connection = sqlite3.connect(DB_NAME)
    try:
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = f"""INSERT INTO tasks
                                  (type, date, title)
                                  VALUES ('{obj['task_type']}', '{obj['task_date']}', '{obj['task_title']}');"""
        cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()
        cursor.close()
    except Exception as e:
        sentry.capture_message(f"[Schedule bot] DB error!\nDesc: {e}")
    finally:
        if sqlite_connection:
            sqlite_connection.close()
