import logging
from logging.config import dictConfig


def configure_logging() -> None:
    """Configure structured logging for the application."""
    dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s',
                }
            },
            'handlers': {
                'default': {
                    'level': 'INFO',
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                }
            },
            'loggers': {
                'uvicorn': {'handlers': ['default'], 'level': 'INFO', 'propagate': False},
                'uvicorn.error': {
                    'handlers': ['default'],
                    'level': 'INFO',
                    'propagate': False,
                },
                'uvicorn.access': {
                    'handlers': ['default'],
                    'level': 'INFO',
                    'propagate': False,
                },
                'app': {'handlers': ['default'], 'level': 'INFO', 'propagate': False},
            },
            'root': {
                'handlers': ['default'],
                'level': 'INFO',
            },
        }
    )


configure_logging()
