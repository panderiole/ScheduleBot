from operator import itemgetter
import sentry_sdk
import schedule
import time

from db import get_all_tasks
from settings import SENTRY_TOKEN

sentry_sdk.init(SENTRY_TOKEN, traces_sample_rate=1.0)


async def get_tasks(type):
    data = await get_all_tasks(sentry_sdk)
    arr = []
    for obj in data:
        if type == obj[1]:
            arr.append(obj)
    arr = sorted(arr, key=itemgetter(4))
    if len(arr) == 0:
        return []
    final_arr = [[arr[0]]]
    for i in range(1, len(arr)):
        if arr[i - 1][4] == arr[i][4]:
            final_arr[len(final_arr) - 1].append(arr[i])
        else:
            final_arr.append([arr[i]])
    return final_arr


def notification_morning():
    pass


def notification_evening():
    pass


def life_cycle():
    schedule.every().day.at("09:00").do(notification_morning)
    schedule.every().day.at("22:30").do(notification_evening)


while True:
    schedule.run_pending()
    time.sleep(1)