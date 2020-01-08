"""Main module."""
import json
import logging

from . import helpers
from .defaults import ACL


class centrallog(logging.getLoggerClass()):
    """centrallog(self, name)
    Custom Logger class which extends the functionality of the existing
    Logger. 'name' is the name of logger. Do not instantiate this class
    direcly instead use getLogger() statid method of the class.
    The 'acl' parameter in most of the function is Access Control List,
    which tells whether the log is for developer(1), support(2) or
    customer(4).

    -------------------------------------------------------------------
    Usage:
    from myoperator.centrallog import centrallog
    logger = centrallog.getLogger()
    logger.log('test.', acl=4)
    -------------------------------------------------------------------

    Additional methods defined:

    dlog(self, level, msg, *args, **kwargs)
        Write developer logs.

    slog(self, level, msg, *args, **kwargs)
        Write support logs.

    clog(self, level, msg, *args, **kwargs)
        Write customer logs.
    """
    _SERVICENAME = None
    _HOSTNAME = ''
    _UID = ''

    def __init__(self, name):
        logging.Logger.__init__(self, name)

    @staticmethod
    def getLogger(name=None):
        if centrallog._SERVICENAME is None:
            # default configuration if not configured yet
            centrallog.configure(name or 'root')
        return logging.getLogger(name)

    @staticmethod
    def basicConfig(**kwargs):
        logging.basicConfig(**kwargs)

    @staticmethod
    def configure(servicename: str, hostname='', uid=''):
        if isinstance(servicename, str):
            centrallog._SERVICENAME = servicename
            centrallog._HOSTNAME = hostname or helpers.get_host_IP()
            centrallog._UID = uid or helpers.get_uuid()
        else:
            raise ValueError("Service name must be a string.")

    @staticmethod
    def get_configuration():
        """Get the configurations set by configure() method"""
        return (centrallog._SERVICENAME, centrallog._HOSTNAME, centrallog._UID)

    @staticmethod
    def is_configured():
        """Check if configurations are already set."""
        return centrallog._SERVICENAME is not None

    def process(self, msg, kwargs):
        """Format the message captured for every log.
        """
        acl = kwargs.pop('acl', ACL['developer'])
        acl_values = set(ACL.values())
        if acl not in acl_values:
            raise ValueError("Invalid acl value. Possible values are %s."
                             % list(acl_values))

        msg_body = {
            "time": "epoch time",
            "mc_time": "epoch ms",
            "ip": centrallog._HOSTNAME,
            "service": centrallog._SERVICENAME,
            "class": "class name",
            "data": {
                "uid": centrallog._UID,
                "msg": msg or '',
                "acl": acl
            },
            "title": "title here...",
        }
        return ("\n" + json.dumps(msg_body, indent=4)), kwargs

    def dlog(self, level, msg, *args, **kwargs):
        """
        Delegate the developer log to the underlying logger.
        """
        kwargs['acl'] = ACL['developer']
        self._log(level, msg, args, **kwargs)

    def slog(self, level, msg, *args, **kwargs):
        """
        Delegate the support log to the underlying logger.
        """
        kwargs['acl'] = ACL['support']
        self._log(level, msg, args, **kwargs)

    def clog(self, level, msg, *args, **kwargs):
        """
        Delegate the customer log to the underlying logger.
        """
        kwargs['acl'] = ACL['customer']
        self._log(level, msg, args, **kwargs)

    def _log(self, level, msg, args, **kwargs):
        """All log dispatcher (overridden method).
        """
        msg, kwargs = self.process(msg, kwargs)
        super()._log(level, msg, args, **kwargs)


logging.setLoggerClass(centrallog)
