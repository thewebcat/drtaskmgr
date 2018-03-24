#!/usr/bin/env python3
import datetime
from time import sleep
from rq import RedisQueue
from threading import Thread
from app import db
from app.models import Task
from config import QUEUE_LABEL, WORKER_THREADS


q = RedisQueue(QUEUE_LABEL)


def task_notify(item: Task(), stop=False):
    """
    Update model Task before and after work done

    :param item: Task() instance
    :type stop: bool
    """
    if item and isinstance(item, Task):
        if not stop:
            item.start_time = datetime.datetime.now()
            print('Work {} start'.format(item.id))
        else:
            item.exec_time = datetime.datetime.now()
            print('Work {} stop'.format(item.id))
        db.session.add(item)
        db.session.commit()


def do_work(item: int):
    """
    THis method runs arbitrary code

    :type item: int
    """
    task = Task.query.get(int(item))
    task_notify(task)

    """START Working code"""
    import time
    import random
    time.sleep(random.randint(15, 25))
    """END Working code"""

    task_notify(task, stop=True)


def worker():
    """Main worker"""
    while True:
        if not q.empty():
            item = q.get()
            do_work(item)
            q.task_done()
        else:
            sleep(0.2)


def main():
    print('Starting Dr.Web Task Manager...')

    for i in range(WORKER_THREADS):
        t = Thread(target=worker, name='worker-{}'.format(i))
        t.daemon = True
        t.start()
        print('Worker {} started'.format(i))

    q.block()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
