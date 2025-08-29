import socket

def get_local_ip():
    """Return the local IP address (for LAN access)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # connect to Google DNS
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
