import threading

class test():

    def test1(self, parma1):
        print("test1" + parma1)

    def test2(self):
        print("test2")

    def test_exe(self):
        exec("self.test1('weird')")


def random_sleep():
    import time
    import random
    time.sleep(random.uniform(1,10))


def thread_test():
    print("thread_test")
    threading.Thread(target=random_sleep()).start()
    threading.Thread(target=random_sleep()).start()
    threading.Thread(target=random_sleep()).start()


if __name__ == '__main__':
    cl = test()
    cl.test_exe()