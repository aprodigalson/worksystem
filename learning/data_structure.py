# 数据结构
class DataStructure(object):
    def __init__(self):
        # 线性表， 栈，队列， 树， 二叉树， 图，
        # 查找， 排序
        # 算法
        pass


from collections import deque
import time
from worksystem.common.utils import Utils
class LinearTable(object):
    # 线性表
    def test_deque(self, length):
        start = time.time()
        queue = deque()
        while True:
            if len(queue) > length:
                break
            queue.append('1')
        end = time.time()
        times = format(end - start, '.6f')
        return times

    def test(self):
        num = 1
        all_list = []
        for num in range(100):
            times = self.test_deque(num)
            tmp_data = {
                'nums': num,
                'times': times
            }
            all_list.append(tmp_data)

        for _ in range(100):
            times = self.test_deque(num)
            tmp_data = {
                'nums': num,
                'times': times
            }
            all_list.append(tmp_data)
            num +=100

        all_list.sort(key=lambda info: info.get('nums'))
        Utils.write_json_file(all_list, './data.json')

if __name__ == '__main__':
    LinearTable().test()
