import math

class Number(object):
    # 无穷
    infinity = '∞'
    # 正无穷
    infinity_positive = '+' + infinity
    # 负无穷
    infinity_negative = '-' + infinity


class Operator(object):
    '''
    运算 ：二元 加减乘除，
          一元 幂， 对数
    '''
    addition = '+'
    @staticmethod
    def add(a, b): return a + Operator.addition + b

    subtraction = '-'
    @staticmethod
    def sub(a, b): return a + Operator.subtraction + b

    multiplication = 'x'
    @staticmethod
    def multi(a, b): return a + Operator.multiplication + b

    division = '/'
    @staticmethod
    def div(a,b): return a + Operator.division + b


    idempotent = '*'
    @staticmethod
    def idemp(a,b): return a + Operator.idempotent + b

    logarithm = 'log'
    @staticmethod
    def log(a,b ): return math.log(a, base=b)

class Set(object):
    '''
    集合
    '''
    pass


class Function(object):

    def __init__(self, define_domain, correspondenc_rule, codomain=None):
        pass
