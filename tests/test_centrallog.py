#!/usr/bin/env python

"""Tests for `centrallog` package."""
import json
import logging
import time
import pytest

from myoperator.centrallog import centrallog, ACL


def get_message_body(caplog):
    """Return the recently logged message body in json format.
    """
    logmsg = caplog.messages
    return json.loads(logmsg[0])

# ---------------------------------------------------------------
#      Builtin funcitonality tests
# ---------------------------------------------------------------


def test_default_logger():
    """Test functioality of default/root logger.
    Check if getLogger is working fine or not.
    """
    logger = centrallog.getLogger()
    assert logger.parent is None, \
        "Root logger must not have any parent logger."

    assert logger.name == 'root', "Name of default logger must be root"


def test_core_logging_functions(logger, caplog):
    """Tests for builtin logger's functions.
    """
    # critical function
    caplog.clear()
    logger.critical("message", acl=ACL['developer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.CRITICAL)

    # error function
    caplog.clear()
    logger.error("message", acl=ACL['customer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.ERROR)

    # warning function
    caplog.clear()
    logger.warning("message", acl=ACL['developer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.WARNING)

    # info function
    caplog.clear()
    logger.info("message", acl=ACL['customer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.INFO)

    # debug function
    caplog.clear()
    logger.debug("message", acl=ACL['developer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.DEBUG)

    # log function
    caplog.clear()
    logger.log(logging.CRITICAL, "message", acl=ACL['support'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.CRITICAL)

def test_logging_epoch(logger, caplog, monkeypatch): 
    monkeypatch.setattr(time, "time", lambda: 1234.567)
    caplog.clear()
    logger.log(logging.CRITICAL, "message", acl=ACL['support'])
    data = get_message_body(caplog)
    assert 1234 == data['time']
    assert 1234.567 == data['mc_time']


# ---------------------------------------------------------------
#      New added funcitonality tests
# ---------------------------------------------------------------


def test_new_added_functions_default_acl(logger, caplog):
    """Tests for new added functions dlog, slog and clog.
    Test their default acl value is logged correctly.
    """
    # dlog function
    caplog.clear()
    logger.dlog(logging.INFO, "message")
    data = get_message_body(caplog)
    assert data['data']['acl'] == ACL['developer'], \
        f"Acl for dlog should be {ACL['developer']}."

    # slog function
    caplog.clear()
    logger.slog(logging.DEBUG, "message")
    data = get_message_body(caplog)
    assert data['data']['acl'] == ACL['support'], \
        f"Acl for slog should be {ACL['support']}."

    # clog function
    caplog.clear()
    logger.clog(logging.ERROR, "message")
    data = get_message_body(caplog)
    assert data['data']['acl'] == ACL['customer'], \
        f"Acl for clog should be {ACL['customer']}."


def test_invalid_acl_value(logger, caplog):
    with pytest.raises(ValueError) as ex:
        logger.error('Err..', acl=-100)  # invalid acl value

    assert str(ex.value).startswith('Invalid acl value')


def test_newlog_functions_default_acl(logger, caplog):
    """Test to check if the new functions dlog, slog and
    clog maintain their default acl values on setting it
    explicitly. These functions should silently discard acl arg.
    """
    # explicitly set acl value for dlog
    caplog.clear()
    logger.dlog(logging.INFO, 'message.', acl=2)
    data = get_message_body(caplog)
    assert data['data']['acl'] == ACL['developer'], \
        f"Acl for dlog should be {ACL['developer']}."

    # explicitly set acl value for slog
    caplog.clear()
    logger.slog(logging.INFO, 'message.', acl=5)
    data = get_message_body(caplog)
    assert data['data']['acl'] == ACL['support'], \
        f"Acl for slog should be {ACL['support']}."

    # explicitly set acl value for clog
    caplog.clear()
    logger.clog(logging.INFO, 'message.', acl=3)
    data = get_message_body(caplog)
    assert data['data']['acl'] == ACL['customer'], \
        f"Acl for clog should be {ACL['customer']}."


def test_configure_without_servicename():
    """Confiure function takes 1 positional arg which should
    be string type.
    """
    with pytest.raises(TypeError):
        centrallog.configure()  # configure without servicename

    with pytest.raises(ValueError):
        centrallog.configure(None)  # servicename other than string


# ----------------------------------------------------------------------------
#       exception in log tests
# ----------------------------------------------------------------------------

def test_exception_log_traceback(logger, caplog):
    """Test exception() logging exception in msg body.
    """
    caplog.clear()
    try:
        raise ValueError('must be logged.')
    except ValueError:
        logger.exception('This should be written.', acl=ACL['developer'])
    data = get_message_body(caplog)

    assert "exception" in data['data'], "Failed to catch exception."
    assert 'This should be written.' == data['data']['msg']
    assert data['data']['exception']['type'] == 'ValueError', \
        'Must catch ValueError.'


def test_exception_log_traceback_in_single_line(logger, caplog):
    """Test traceback by exception function is logged in single line.
    """
    caplog.clear()
    try:
        raise ValueError('must be logged.')
    except ValueError:
        logger.exception('This should be written.', acl=ACL['developer'])
    data = get_message_body(caplog)
    assert 'ValueError: must be logged.' in data['data']['exception']['traceback']
    assert '\n' not in data['data']['exception']['traceback'], \
        "Tracelog should not contain '\n', it should be in single line."


def test_log_title(logger, caplog):
    """Test logger's title functionality.
    """
    # set title using chaining
    caplog.clear()
    logger.title('Xoxo').dlog(logging.ERROR, 'message')
    data = get_message_body(caplog)
    assert data['title'] == 'Xoxo', 'Title must be same as set in logger'

    # set title using keyword arg in log function
    caplog.clear()
    logger.dlog(logging.ERROR, 'message', title='tItLe')
    data = get_message_body(caplog)
    assert data['title'] == 'tItLe', 'Title must be same as title keyword.'


def test_title_preference(logger, caplog):
    """Title for a log can be set using two methods.
    Either using title() method or using 'title' keyword.
    On using both keyword must be higher precedence.
    """
    caplog.clear()
    logger.title('Xoxo').dlog(logging.ERROR, 'message', title='Yolo')
    data = get_message_body(caplog)
    assert data['title'] == 'Yolo', 'title keyword high precedence.'
    assert data['title'] != 'Xoxo', 'title method low precedence.'
