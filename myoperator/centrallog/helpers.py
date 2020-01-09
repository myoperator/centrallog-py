import io
import traceback
import socket
import uuid


def get_host_IP():
    """Function to get host IP address."""
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
        return host_ip
    except Exception:
        return ""


def get_uuid():
    """Returns a uuid in hex format."""
    return uuid.uuid1().hex


def get_exception_traceback(exc_info: tuple):
    """Get exception traceback from sys.exc_info() tuple."""
    sio = io.StringIO()
    tb = exc_info[2]
    traceback.print_exception(exc_info[0], exc_info[1], tb, None, sio)
    s = sio.getvalue()
    sio.close()
    if s[-1:] == "\n":
        s = s[:-1]
    return s
