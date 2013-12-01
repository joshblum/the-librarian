import os

# APIs
TMDB_API_KEY = "04a87a053afac639272eefbb94a173e4"
OMDB_API_URL = "http://www.omdbapi.com/"

PROGRESS = 1000
MAX_PROCESSES = 4

# server
HOST = "127.0.0.1"
PORT = 6885
DEBUG = True

# metastore
DEFAULT_DB = "librarian"
DEFAULT_JOB_COLLECTION = "jobs"
DEFAULT_META_COLLECTION = "entity_meta"

#job progress tracking
JOB_ENQUEUED = "enqueued"
JOB_STARTED =JOB_ENQUEUED# "started"
JOB_INPROGRESS =JOB_ENQUEUED# "in-progress"
JOB_FAILED =JOB_ENQUEUED# "failed"
JOB_COMPLETED =JOB_ENQUEUED# "completed"

#ENTITY_TYPES
ENTITY_MOVIE = "movie"

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
WORKSPACE_PATH = os.path.join(ROOT_PATH, ".librarian")

VIDEO_EXT = set([
    '3g2', '3gp', '3gp2', '3gpp', '60d', 'ajp', 'asf', 'asx', 'avchd', 'avi', 'bik', 'bix', 'box', 'cam', 'dat', 'divx', 'dmf', 'dv', 'dvr-ms', 'evo', 'flc', 'fli', 'flic', 'flv', 'flx', 'gvi', 'gvp', 'h264', 'm1v', 'm2p', 'm2ts', 'm2v', 'm4e', 'm4v', 'mjp', 'mjpeg', 'mjpg',
    'mkv', 'moov', 'mov', 'movhd', 'movie', 'movx', 'mp4', 'mpe', 'mpeg', 'mpg', 'mpv', 'mpv2', 'mxf', 'nsv', 'nut', 'ogg', 'ogm', 'omf', 'ps', 'qt', 'ram', 'rm', 'rmvb', 'swf', 'ts', 'vfw', 'vid', 'video', 'viv', 'vivo', 'vob', 'vro', 'wm', 'wmv', 'wmx', 'wrap', 'wvx', 'wx', 'x264', 'xvid'])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': '%s/log.log' % WORKSPACE_PATH,
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}
