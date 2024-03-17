import logging.config
import yaml
import os

with open('./config/logger_config.yaml', 'rt') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)

# Get a logger object
logger = logging.getLogger('development')