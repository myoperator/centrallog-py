#!/usr/bin/env python

"""Tests for `centrallog` package."""
import json
import logging
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
    """Tests for builtin logger's functoins.
    """
    # critical function
    logger.critical("message", acl=ACL['developer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.CRITICAL)
    caplog.clear()

    # error function
    logger.error("message", acl=ACL['customer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.ERROR)
    caplog.clear()

    # warning function
    logger.warning("message", acl=ACL['developer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.WARNING)
    caplog.clear()

    # info function
    logger.info("message", acl=ACL['customer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.INFO)
    caplog.clear()

    # debug function
    logger.debug("message", acl=ACL['developer'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.DEBUG)
    caplog.clear()

    # log function
    logger.log(logging.CRITICAL, "message", acl=ACL['support'])
    record_tuple = caplog.record_tuples[0]
    assert record_tuple[:-1] == (logger.name, logging.CRITICAL)
    caplog.clear()


# ---------------------------------------------------------------
#      New added funcitonality tests
# ---------------------------------------------------------------


def test_new_added_functions_default_acl(logger, caplog):
    """Tests for new added functions dlog, slog and clog.
    Test their default acl value is logged correctly.
    """
    # dlog function
    logger.dlog(logging.INFO, "message")
    data = get_message_body(caplog)
    assert data['data']['acl'] == ACL['developer'], \
        f"Acl for dlog should be {ACL['developer']}."
    caplog.clear()

    # slog function
    logger.slog(logging.DEBUG, "message")
    data = get_message_body(caplog)
    assert data['data']['acl'] == ACL['support'], \
        f"Acl for slog should be {ACL['support']}."
    caplog.clear()

    # clog function
    logger.clog(logging.ERROR, "message")
    data = get_message_body(caplog)
    assert data['data']['acl'] == ACL['customer'], \
        f"Acl for clog should be {ACL['customer']}."
    caplog.clear()


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
    logger.dlog(logging.INFO, 'message.', acl=2)
    data = get_message_body(caplog)
    caplog.clear()
    assert data['data']['acl'] == ACL['developer'], \
        f"Acl for dlog should be {ACL['developer']}."

    # explicitly set acl value for slog
    logger.slog(logging.INFO, 'message.', acl=5)
    data = get_message_body(caplog)
    caplog.clear()
    assert data['data']['acl'] == ACL['support'], \
        f"Acl for slog should be {ACL['support']}."

    # explicitly set acl value for clog
    logger.clog(logging.INFO, 'message.', acl=3)
    data = get_message_body(caplog)
    caplog.clear()
    assert data['data']['acl'] == ACL['customer'], \
        f"Acl for clog should be {ACL['customer']}."


def test_configure_without_servicename():
    """confiure function takes 1 positional arg which should
    be string type.
    """
    with pytest.raises(TypeError):
        centrallog.configure()  # configure without servicename

    with pytest.raises(ValueError):
        centrallog.configure(None)  # servicename other than string


# ----------------------------------------------------------------------------
#       log message formatting test cases
# ----------------------------------------------------------------------------


def flattern_values(msg):
    """Get all the values of a json into a list.
    """
    data = []
    if isinstance(msg, list):
        for m in msg:
            fv = flattern_values(m)
            data += fv
    elif isinstance(msg, dict):
        for m in msg.values():
            fv = flattern_values(m)
            data += fv
    else:
        data.append(msg)
    return data


def contains_null_falsy_value(msg):
    """Check if any value contains null or falsy except empty string.
    Return true if contains.
    """
    vals = flattern_values(msg)
    vals = [v for v in vals if not isinstance(v, str)]
    return not all(vals)


def test_nullable_falsy_values_in_message(logger, caplog):
    logger.warning(None)
    data = get_message_body(caplog)

    assert not contains_null_falsy_value(data), \
        "Log message contains falsy value other than empty string."


@pytest.mark.skip(reason="no way of currently testing this")
def test_demo(logger, caplog):
    # test funciton
    logger.clog(logging.ERROR, 'netlog')
    txt = caplog.text
    assert 'log' == txt
