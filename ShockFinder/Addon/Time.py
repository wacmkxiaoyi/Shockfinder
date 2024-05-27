# File type: <Function> set
# By Junxiang H., 2023/07/2
# wacmk.com/cn Tech. Supp.

import datetime, time


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_time():
    return time.time()


def sleep(sec):
    time.sleep(sec)
