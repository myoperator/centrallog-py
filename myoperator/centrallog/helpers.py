import socket
import uuid


def get_host_IP():
    """Function to get host IP address."""
    try:
        host_ip = socket.gethostbyname(gethostname())
        return host_ip
    except Exception:
        return ""


def get_uuid():
    """Return a uuid."""
    return uuid.uuid1().hex
