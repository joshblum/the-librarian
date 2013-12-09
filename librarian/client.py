from constants import HOST, PORT, ENTITY_MOVIE, LOGGING
import requests
import glob
import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

PATH = "/bomber/media/Movies/Other/"
URL = "http://%s:%s" % (HOST, PORT)


def get_url(path):
    return "%s/%s" % (URL, path)


def get_paths(path=PATH):
    return glob.glob("%s*" % path)


def add_job(srcpath):
    r = requests.get(get_url("entity_drop"), params={
                     'srcpath': srcpath,
                     'entity_type': ENTITY_MOVIE,
                     }).json()
    logger.debug(r)


def check_job(job_id):
    url = get_url("progress")
    r = requests.get("%s/%s" % (url, job_id)).json()
    logger.debug(r)
    return r


def add_jobs(lim=5):
    paths = get_paths()
    for i, path in enumerate(paths):
        logger.debug("Adding %s to job queue" % path)
        add_job(path)
        if i > lim:
            break

if __name__ == "__main__":
    add_jobs()
