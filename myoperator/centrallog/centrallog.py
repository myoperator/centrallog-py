"""Main module."""
# import logging
import json

import logging


ACL = {
    "developer": 1,
    "support": 2,
    "customer": 4,
}


class centrallog(logging.getLoggerClass()):
    def __init__(self, name):
        logging.Logger.__init__(self, name)

    @staticmethod
    def getLogger(name='root'):
        return logging.getLogger(name)

    @staticmethod
    def basicConfig(**kwargs):
        logging.basicConfig(**kwargs)

    def process(self, msg, kwargs):
        """Format the message captured for every log.
        """
        acl = kwargs.pop('acl', ACL['developer'])
        acl_values = ACL.values()
        if acl not in acl_values:
            raise ValueError("Invalid acl value. Possible values are %s."
                             % list(acl_values))

        msg_body = {
            "time": "epoch time",
            "mc_time": "epoch ms",
            "ip": "server-ip",
            "class": "class name",
            "data": {
                "uid": "uid",
                "msg": msg,
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
