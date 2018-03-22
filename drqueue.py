# -*- coding: utf-8 -*-

from queue import Queue
from threading import Thread

import time

num_worker_threads = 2

q = Queue()


def do_work(item):
    import time
    import random
    print('Work {} start'.format(item))
    time.sleep(random.randint(0, 15))
    print('Work {} complete'.format(item))


def worker():
    while True:
        if not q.empty():
            item = q.get()
            do_work(item)
            q.task_done()


def source():
    for i in range(100, 103):
        yield i


def main():
    print("Starting Dr.Web Task Manager...")

    for i in range(num_worker_threads):
        t = Thread(target=worker, name='worker-{}'.format(i))
        t.daemon = True
        t.start()
        print('Worker {} started'.format(i))

    for item in source():
        time.sleep(2)
        q.put(item)

    q.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
