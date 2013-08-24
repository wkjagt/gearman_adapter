import gearman, pickle

servers = ['localhost:4730']

class PickleDataEncoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return pickle.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return pickle.loads(decodable_string)

class Client(gearman.GearmanClient):
    data_encoder = PickleDataEncoder


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
    return Client(servers)

def get_worker():
    return Worker(servers)
