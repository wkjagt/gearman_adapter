import gearman, pickle
import sentinelapp.settings
from gearman.constants import PRIORITY_NONE

class PickleDataEncoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return pickle.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return pickle.loads(decodable_string)

class Client(gearman.GearmanClient):
    data_encoder = PickleDataEncoder

    def submit_async_job(self, task, data, unique=None, priority=PRIORITY_NONE, background=False, max_retries=0, poll_timeout=None):
        return super(Client, self).submit_job(task, data, unique=unique, priority=priority, background=background, wait_until_complete=False, max_retries=0, poll_timeout=None)

class Worker(gearman.GearmanWorker):

    data_encoder = PickleDataEncoder

    def on_job_execute(self, current_job):
        task = current_job.task
        data = current_job.data

        print "======================================"
        print "---------------- TASK ----------------"
        print task
        print "---------------- DATA ----------------"
        print data
        print "======================================"

        return super(Worker, self).on_job_execute(current_job)

    def on_job_exception(self, current_job, exc_info):
        return super(Worker, self).on_job_exception(current_job, exc_info)

    def on_job_complete(self, current_job, job_result):
        return super(Worker, self).send_job_complete(current_job, job_result)

    def after_poll(self, any_activity):
        # Return True if you want to continue polling, replaces callback_fxn
        return True


def get_client():
    return Client(sentinelapp.settings.GEARMAN_SERVERS)

def get_worker():
    return Worker(sentinelapp.settings.GEARMAN_SERVERS)
