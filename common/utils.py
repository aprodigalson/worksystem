import random
import string
import casbin
import time
import json
import os

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


if __name__ == '__main__':
    pass
