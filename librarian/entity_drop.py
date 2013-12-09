"""
    Endpoint to handle the absorption of entities.
    Has a queue of jobs to process and runs each job within a new 
    process.
    Client can query job progress via the srcpath provided
"""

from handlers import handlers
from metastore import MetaCon
from constants import MAX_PROCESSES, ENTITY_MOVIE, LOGGING

from multiprocessing import Process, Queue
from threading import Thread

import logging.config

import time

SLEEP = 5

ENTITY_MAP = {
    ENTITY_MOVIE: handlers.MovieHandler,
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def process_entity(q):
    while True:
        job = q.get()
        handler = ENTITY_MAP.get(
            job['entity_type'], handlers.DummyHandler)(
                job['job_id'], job['srcpath'], job['entity_type'])
        handler.run()


def entity_queue():
    metacon = MetaCon()
    q = Queue()

    for _ in xrange(MAX_PROCESSES):
        p = Process(target=process_entity, args=(q,))
        p.start()

    logger.info("Waiting for new jobs.")

    while True:

        jobs = metacon.find_enqueued_jobs()

        for job in jobs:
            logger.debug("Found job %s" % job)
            q.put(job)
        time.sleep(SLEEP)

if __name__ == "__main__":
    t = Thread(target=entity_queue)
    t.start()
