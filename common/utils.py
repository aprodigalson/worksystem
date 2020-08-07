import random
import string
class Utils(object):
    pass

class StringUtils(object):
    @staticmethod
    def random_string(length = 3):
        return ''.join(random.sample(string.ascii_letters, length))