#!/usr/bin/env python3
import os
import subprocess
import shlex
import unittest

from config import basedir
from app import app, db
from app.models import Task
from rq import RedisQueue


def run_cmd(cmd):
    """Run a command and return a tuple with (stdout, stderr, exit_code)"""
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate()
    return stdout, stderr, process.wait()


class TaskTestCase(unittest.TestCase):

    def setUp(self):
        # app.config
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        db.create_all()
        (o, e, s) = run_cmd('flask db upgrade')
        self.assertTrue(s == 0)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_task(self):
        t = Task()
        db.session.add(t)
        db.session.commit()
        self.assertTrue(t.id)

    def test_routes(self):
        with app.test_client() as c:
            response = c.get('/')
            self.assertEqual(response.status_code, 302)

            response = c.get('/api/v1.0/tasks')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            response = c.post('/api/v1.0/tasks')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            response = c.get('/api/v1.0/tasks/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            response = c.get('/api/v1.0/tasks/gtr')
            self.assertEqual(response.status_code, 404)

    def test_rq(self):
        q = RedisQueue('test')
        self.assertTrue(q.empty())
        self.assertEqual(q.qsize(), 0)
        q.put('test')
        self.assertEqual(q.qsize(), 1)
        self.assertEqual(q.get(), b'test')

    def test_rqmanager(self):
        from rqmanager import task_notify





if __name__ == '__main__':
    unittest.main()
