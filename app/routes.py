from flask import jsonify, redirect, url_for

from app import app, db
from app.models import Task
from rq import RedisQueue


@app.route('/')
def home():
    return redirect(url_for('get_tasks'))


@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    output = []
    tasks = Task.query.all()
    for task in tasks:
        output.append({
            'id': task.id,
            'create_time': task.create_time,
            'start_time': task.start_time,
            'exec_time': task.exec_time
        })
    return jsonify({'tasks': output})


@app.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.create_time and not task.start_time and not task.exec_time:
        status = 'In Queue'
    elif task.start_time and not task.exec_time:
        status = 'Run'
    else:
        status = 'Completed'

    try:
        exec_time = task.exec_time - task.start_time
    except TypeError:
        exec_time = None
    else:
        exec_time = '{0}:{1}:{2}'.format(divmod(exec_time.seconds, 3600)[0], divmod(exec_time.seconds, 60)[0],
                                         exec_time.seconds)
    return jsonify({
        'status': status,
        'create_time': task.create_time,
        'start_time': task.start_time,
        'time_to_execute': exec_time,
    })


@app.route('/api/v1.0/tasks', methods=['POST'])
def add_task():
    task = Task()
    db.session.add(task)
    db.session.commit()
    q = RedisQueue('drwebtaskmgr')
    q.put(task.id)
    return jsonify({'task': task.id})
