"""
    Endpoint to handle the absorption of entities.
    Has a queue of jobs to process and runs each job within a new 
    process.
    Client can query job progress via the srcpath provided
"""

from handlers import handlers

from constants import MAX_PROCESSES

from multiprocessing import Process, Queue
from threading import Thread

SLEEP = 5

ENTITY_MAP = {
    'movie' : handlers.MovieHandler,
}

def process_entity():
    while True:
        srcpath, job_id, entity_type = q.get()
        handler = ENTITY_MAP.get(entity_type, handlers.DummyHandler)(srcpath, job_id)
        handler.run()
        q.task_done()

def entity_queue():

    q = Queue()
    for _ in xrange(MAX_PROCESSES):
         p = Process(target=process_entity, args=(q,))
         p.start()

    # while True:
        #get item from metastore
        # q.put((srcpath, entity_type))
        # time.sleep(SLEEP)

    q.join()       # block until all tasks are done

if __name__ == "__main__":
    t = Thread(target=entity_queue)
    t.start()