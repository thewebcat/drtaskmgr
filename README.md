drtaskmgr
========

Usage
-----

Install `redis-server`

Install all requirements:

    pip install -r requirements.txt


Launch rqmanager:

    ./rqmanager.py

API Usage
---------

Add task in queue:

    post: /api/v1.0/tasks

```
{
    "task": 33
}
```

View all tasks:

    get: /api/v1.0/tasks

```
{
    "tasks": [
        {
            "create_time": "Thu, 22 Mar 2018 22:54:28 GMT",
            "exec_time": "Fri, 23 Mar 2018 01:54:46 GMT",
            "id": 8,
            "start_time": "Fri, 23 Mar 2018 01:54:28 GMT"
        },
        {
            "create_time": "Thu, 22 Mar 2018 22:55:59 GMT",
            "exec_time": "Fri, 23 Mar 2018 01:56:14 GMT",
            "id": 9,
            "start_time": "Fri, 23 Mar 2018 01:55:59 GMT"
        }
    ]
}
```

Get detail information about task:

    get: /api/v1.0/tasks/<task_id>

```
{
    "create_time": "Sat, 24 Mar 2018 17:24:26 GMT",
    "start_time": "Sat, 24 Mar 2018 17:52:21 GMT",
    "status": "Completed",
    "time_to_execute": "0:0:25"
}
```
