import logging
from logging.config import dictConfig

logger_level = logging.INFO

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": logger_level,
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app": {"handlers": ["console"], "level": logger_level, "propagate": False},
    },
    "root": {"handlers": ["console"], "level": logger_level},
}

dictConfig(log_config)
logger = logging.getLogger()
