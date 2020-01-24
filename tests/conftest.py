import logging
import pytest

from myoperator.centrallog import centrallog


@pytest.fixture()
def logger():
    FORMAT = '%(name)s: (%(asctime)s) [%(levelname)s] - %(message)s'
    centrallog.basicConfig(format=FORMAT)
    logger = centrallog.getLogger('testlogger')
    logger.setLevel(logging.DEBUG)
    return logger
