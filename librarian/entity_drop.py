"""
    Endpoint to handle the absorption of entities.
    Has a queue of jobs to process and runs each job within a new 
    process.
    Client can query job progress via the srcpath provided
"""

from handlers import handlers
from metastore import MetaCon
from constants import MAX_PROCESSES, ENTITY_MOVIE

from multiprocessing import Process, Queue
from threading import Thread

SLEEP = 5

ENTITY_MAP = {
    MOVIE_TYPE: handlers.MovieHandler,
}


def process_entity():
    while True:
        job = q.get()
        handler = ENTITY_MAP.get(
            job['entity_type'], handlers.DummyHandler)(job['srcpath'], job['job_id'])
        handler.run()
        q.task_done()


def entity_queue():
    metacon = MetaCon()
    q = Queue()
    for _ in xrange(MAX_PROCESSES):
        p = Process(target=process_entity, args=(q,))
        p.start()

    while True:
        jobs = metacon.get_enqueued_jobs()
        for job in jobs:
            q.put(job)
        time.sleep(SLEEP)
    
    # # block until all tasks are done
    # q.join()       

if __name__ == "__main__":
    t = Thread(target=entity_queue)
    t.start()
