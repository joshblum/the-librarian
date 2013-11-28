import os

TMDB_API_KEY = "04a87a053afac639272eefbb94a173e4"
OMDB_API_URL = "http://www.omdbapi.com/"
PROGRESS = 1000

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

WORKSPACE_PATH = os.path.join(ROOT_PATH, ".librarian")

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
