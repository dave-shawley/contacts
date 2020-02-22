import logging
import os
import pathlib
import sys


def setup_package():
    logger = logging.getLogger('setup_package')
    this_dir = pathlib.Path(__file__).absolute().parent
    env_file = this_dir.parent / 'build' / 'test-environment'
    if not env_file.exists():
        logger.error('Environment file not found at %s', env_file)
        logger.error('Did you forget to run the bootstrap script?')
        sys.exit(-1)

    logger.info('loading environment variables from %s', str(env_file))
    for line in env_file.read_text().splitlines(keepends=False):
        name, _, value = line.strip().partition('=')
        if value.startswith(('"', "'")) and value.endswith(value[0]):
            value = value[1:-1]
        name = name.upper()
        logger.debug('setting environment variable %s=%s', name, value)
        os.environ[name] = value
