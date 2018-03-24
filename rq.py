import threading

import redis


class RedisQueue(object):
    """
    Redis Queue
    """
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)

        self.mutex = threading.Lock()
        self.all_tasks_done = threading.Condition(self.mutex)
        self.unfinished_tasks = 0

    def qsize(self):
        """Return size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if queue is empty, False if not."""
        with self.mutex:
            return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)
        self.unfinished_tasks += 1

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.
        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)
        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

    def task_done(self):
        """
        TODO: not working with redis
        """
        pass
        # with self.all_tasks_done:
        #     unfinished = self.unfinished_tasks - 1
        #     if unfinished <= 0:
        #         if unfinished < 0:
        #             raise ValueError('task_done() called too many times')
        #         self.all_tasks_done.notify_all()
        #     self.unfinished_tasks = unfinished

    def block(self):
        """Blocks IO until the Queue Manager is running"""
        with self.all_tasks_done:
            self.all_tasks_done.wait()

    def join(self):
        """Blocks until all items in the Queue have been gotten and processed."""
        with self.all_tasks_done:
            while self.unfinished_tasks:
                self.all_tasks_done.wait()