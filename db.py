import asyncio
import sqlite3
from settings import *


async def execute_command(q, sentry, type):
    records = ''
    sqlite_connection = sqlite3.connect(DB_NAME)
    try:
        cursor = sqlite_connection.cursor()
        cursor.execute(q)
        if type == 'get':
            records = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()
    except Exception as e:
        sentry.capture_message(f"[Schedule bot] DB error!\nDesc: {e}")
    finally:
        if sqlite_connection:
            sqlite_connection.close()
    return records


async def write_task(obj, sentry):
    sqlite_insert_query = f"""INSERT INTO tasks (type, date, title, place, isCompleted)
                              VALUES ('{obj['task_type']}', '{obj['task_date']}', '{obj['task_title']}',
                               '{obj['task_place']}', 0);"""
    await execute_command(sqlite_insert_query, sentry, 'write')


async def get_all_tasks(sentry):
    return await execute_command("""SELECT * from tasks""", sentry, 'get')


async def delete_task(id, sentry):
    await execute_command(f"""DELETE FROM tasks WHERE id={id}""", sentry, 'delete')


def update_task(id, value, sentry):
    asyncio.run(execute_command(f"""UPDATE tasks SET isCompleted={value} WHERE id={id}""", sentry, "update"))
