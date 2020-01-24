==========
centrallog
==========


CentralLog helps recording the logs by MyOperator standards.

The format of the log message is
::

    {
        "time":<unix-epoch>,
        "mc_time":<unix-epoch in microseconds>,
        "ip":"<host-ip-address>",
        "service": <application/service name>,
        "class":"<source class name logging this>",
        "data":{
            "uid":"<unique log identifier>",
            "msg":"<actual message>",
            "acl":<acl numeric representation>
        },
        "title": <logging context provider>
    }

For description please refer to `Documentation <http://docs.myoperator.biz/books/standards/page/technical-documentation>`_.

Features
--------
- Auto-format log message to desired form by simply configuring the logger.

Installation
------------
To install the centrallog package run the following commands::

    $ git clone https://github.com/myoperator/centrallog-py.git
    $ pip install -e centrallog-py

Quickstart
----------

For the impatient:

.. code:: python

    from myoperator.centrallog import centrallog
    FORMAT = '%(name)s: (%(asctime)s) [%(levelname)s] - %(message)s'
    centrallog.basicConfig(format=FORMAT)
    logger = centrallog.getLogger('testlogger')
    logger.error("Log message")

Configurations
--------------
The basic configuration of logger is same as the python's builtin `logging <https://docs.python.org/3.7/library/logging.html>`_ library.

For customizing message-format use the following class methods.

basicConfig(\*\*kwargs)
#######################

    This method is same as the logging's `basicConfig(**kwargs) <https://docs.python.org/3.7/library/logging.html#logging.basicConfig>`_.

configure(servicename, hostname='', uid='')
###########################################

    This method is used to configure the servicename, the hostname, the uuid of the logger throughout the 
    program.

    ``TIP: Use this method once throughout the program before logging any message.``


is_configured()
###############

    Check if a logger is configured and return true if it is configured, else false.

get_configuration()
###################

    Returns the configuration *tuple(servicename, hostname, uid)*.

Logging Methods
---------------
centrallog supports all the log methods of the logging library with an additional optional keyword-argument ``acl`` which shows the relevancy of the log.

The value of acl(Access Control List) can only be one of the following::

    1 - developer (default)
    2 - support
    4 - customer

Example: To log an error message relevant to the customer(acl = 4).

.. code:: python

    logger.error('message', acl=4)


centrallog also provide some additional methods with default acl behaviour.

dlog(level, message, \*args, \*\*kwargs)
########################################
  developer specific log(acl=1).

slog(level, message, \*args, \*\*kwargs)
########################################
  support specific log(acl=2).

clog(level, message, \*args, \*\*kwargs)
########################################
  customer specific log(acl=4).

Loggin with title
#################
  To add a title to the log message centrallog provide one of the two ways.

  Using *title* keyword argument in every log message.

  And using **title(text)** method.

  Example::

    logger.title('title here').dlog('message here')
    logger.warning('message...', title='Title here')

  ``Tip: On using both method and keyword, keyword will get higher precedence.``
  
  For further technical documentation please visit `here <http://docs.myoperator.biz/books/standards/page/technical-documentation>`_.
