# -*- coding:utf-8 -*-


# 通过socket获取本机的ip地址
def get_local_ip():
    import socket
    hostname = socket.gethostname()
    print(socket.gethostbyname(hostname))
# =============================================================


def callback_func(result):
    print('Got result--{}'.format(result))


def add(x, y):
    return x + y


def print_args(func, args, *, callback):
    result = func(*args)
    callback(result)


# 1. 让回调函数访问外部信息，一种方法是使用一个绑定方法来代替一个简单方法；
class ResultHandler():
    def __init__(self):
        self.sequeue = 0

    def handler(self, result):
        self.sequeue += 1
        print("[{}] Got result--{}".format(self.sequeue, result))


# 2. 使用一个闭包捕获状态值
def make_handler():
    sequeue = 0

    def handler(result):
        nonlocal sequeue
        sequeue += 1
        print("[{}] Got result--{}".format(sequeue, result))
    return handler


# 3. 使用协程
def make_handler0():
    sequeue = 0
    while True:
        result = yield
        sequeue += 1
        print("[{}] Got result--{}".format(sequeue, result))
# =============================================================


# 4. 批量创建多个对象
class Person(object):
    def __init__(self, name):
        self.name = name


def create_many_instances():
    print(locals())
    print(globals())
    for i in range(10):
        locals()['dx' + str(i)] = Person('dx%s' % i)
        # print(locals()['dx' + str(i)])
        globals()['xd' + str(i)] = Person('xd%s' % i)
        # print(globals()['xd' + str(i)])
    # print(locals())
    print(globals())
    objectList = [object() for _ in range(1000)]


if __name__ == '__main__':
    create_many_instances()
    # handler = make_handler0() # 3
    # next(handler) # 3
    # print_args(add, (2, 3), callback=handler.send) # 3
    # handler = make_handler() # 2
    # print_args(add, (2, 3), callback=handler) # 2
    # r = ResultHandler()   # 1
    # print_args(add, (3, 2), callback=r.handler) # 1
    # print_args(add, (3, 2), callback=callback_func)



