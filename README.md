Gearman Adapter
===============

Convenient python wrapper for [gearman](http://gearman.org).

Purpose:

1. Have the gearman server address(es) in one place
2. Support sending of python objects to workers
3. Have a slightly shorter way to register asynchronous jobs


###Client usage:

```py
import gearman_wrapper

client = gearman_adapter.get_client()
client.submit_job('some_task', {"key" : "value"}, wait_until_complete=False)
```

###Worker usage

```py
import gearman_adapter

def task_callback(gearman_worker, job):
    """ do something with job.data like send an email """
    return True

worker = gearman_wrapper.get_worker()
worker.register_task('some_task', task_callback)
worker.work()
```
