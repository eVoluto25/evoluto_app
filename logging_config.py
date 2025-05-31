
import logging
import logging.config

def setup_logging():
    logging_config = {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'INFO',
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'formatter': 'standard',
                'level': 'DEBUG',
            },
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    }

    logging.config.dictConfig(logging_config)
