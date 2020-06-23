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


# 根据local()以及global()创建多个实例
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


class Pair(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)
# =============================================================
# 5. 私有属性或方法
class A(object):
    def __init__(self):
        self._internal = 0
        self.public = 1
        self.__private_param = 100

    def public_method(self):
        print(self.__private_method)
        print(self.__private_param)

    def _internal(self):
        pass

    def __private_method(self):
        pass

class B(A):
    def __init__(self):
        super(B, self).__init__()
        self.__private_param = 100

    def __private_method(self):
        pass

# =============================================================
    # 没有显式的指明某个类的父类，super() 仍然可以有效的工作。
class Proxy(object):
    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name.startwith('_'):
            # super() 调用原始的 __setattr__()
            super().__setattr__(name, value)
        else:
            setattr(self._obj, name, value)


# super().__init__()
class Base:
    def __init__(self):
        print('Base.__init__')


class C(Base):
    def __init__(self):
        Base.__init__(self)
        print('C.__init__')


class D(Base):
    def __init__(self):
        Base.__init__(self)
        print('D.__init__')


class E(C,D):
    def __init__(self):
        C.__init__(self)
        D.__init__(self)
        print('E.__init__')


class F(Base):
    def __init__(self):
        super().__init__()
        print("F.__init__")


class G(Base):
    def __init__(self):
        super().__init__()
        print('G.__init__')


class H(F, G):
    def __init__(self):
        super().__init__()
        print("H.__init__")


class I():
    def spam(self):
        super().spam()
        print("I spam")


class J():
    def spam(self):
        print("J spam")


class K(I, J):
    pass

if __name__ == '__main__':
    pass
    # e = E()
    # h = H()
    # print(H.__mro__)
    # print(F.__mro__)
    # k = K()
    # k.spam()

    # a = A()
    # a.public_method()
    # print(a.__dict__)
    # print(a._A__private_param)
    # print(dir(a))
    # b = B()
    # print(dir(b))
    # print(b._A__private_param)

    # p = Pair(4, 6)  #5
    # print("%r" % p, str(p), p, repr(p)) # 5

    # create_many_instances() # 4

    # handler = make_handler0() # 3
    # next(handler) # 3
    # print_args(add, (2, 3), callback=handler.send) # 3

    # handler = make_handler() # 2
    # print_args(add, (2, 3), callback=handler) # 2

    # r = ResultHandler()   # 1
    # print_args(add, (3, 2), callback=r.handler) # 1
    # print_args(add, (3, 2), callback=callback_func)



