import random
import string
import casbin
import time
import json
import os
import datetime
from IPy import IP

class Utils(object):
    @staticmethod
    def count_func_time(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            print(f'{func.__name__} use {(end - start):.6f} secends')
            return res
        return wrapper

    @staticmethod
    def write_json_file(data, file_path, indent=4):
        with open(file_path, 'w') as fp:
            json.dump(data,fp ,indent=4)

class StringUtils(object):
    @staticmethod
    def random_string(length=3):
        return ''.join(random.sample(string.ascii_letters, length))

class DateUtils(object):
    @staticmethod
    def count_date_before_date(start_data=None, days=208):
        if start_data is None:
            start_data = datetime.datetime.now()
        days = datetime.timedelta(days=-days)
        end_data = start_data + days
        return end_data

class IPUtils(object):
    @staticmethod
    def convert_decimal_mask_to_dotted_decimal(mask):
        # turn 24 to 255.255.255.0
        return str(IP('255.255.255.255').make_net(mask).net())

if __name__ == '__main__':
    print(IPUtils.convert_decimal_mask_to_dotted_decimal(30))