import os
basedir = os.path.abspath(os.path.dirname(__file__))

WORKER_THREADS = 2
QUEUE_LABEL = 'drwebtaskmgr'

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
