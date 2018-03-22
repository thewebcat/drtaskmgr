#!/usr/bin/env python3
import datetime
import redis
from queue import Queue
from threading import Thread
from app import db
from app.models import Task


WORKER_THREADS = 2

r = redis.StrictRedis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
q = Queue()


def do_work(item):
    import time
    import random
    task = Task.query.get(int(item))
    print('Work {} start'.format(task.id))
    task.start_time = datetime.datetime.now()
    db.session.add(task)
    db.session.commit()
    '''
    START Working code
    '''
    time.sleep(random.randint(15, 25))
    '''
    END
    '''
    print('Work {} complete'.format(task.id))
    task.exec_time = datetime.datetime.now()
    db.session.add(task)
    db.session.commit()


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

    pubsub.subscribe(['drtaskmgr'])

    for item in pubsub.listen():
        if not item['data'] == 1:
            q.put(item['data'])

    q.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pubsub.unsubscribe()
        print()
