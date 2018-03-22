#!/usr/bin/env python3
import redis
from queue import Queue
from threading import Thread


WORKER_THREADS = 2

r = redis.StrictRedis(host='localhost', port=6379, db=0)
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


def main():
    print("Starting Dr.Web Task Manager...")

    for i in range(WORKER_THREADS):
        t = Thread(target=worker, name='worker-{}'.format(i))
        t.daemon = True
        t.start()
        print('Worker {} started'.format(i))

    pubsub = r.pubsub()
    pubsub.subscribe(['drtaskmgr'])

    for item in pubsub.listen():
        if not item['data'] == 1:
            q.put(item['data'])

    q.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
