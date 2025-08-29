import http.server
import socketserver
import threading
from functools import partial  # for specifying folder

_server = None

def start_server(folder, port=5000):
    """
    Starts a HTTP server serving 'folder' on given port.
    If port is busy, picks a free port automatically.
    Returns the actual port used.
    """
    global _server

    # Use handler with directory explicitly set
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=folder)

    # Try to bind, fallback to free port if busy
    try:
        _server = socketserver.TCPServer(("", port), handler)
    except OSError:
        # Port busy, auto-pick
        _server = socketserver.TCPServer(("", 0), handler)

    actual_port = _server.server_address[1]

    # Run server in background thread
    thread = threading.Thread(target=_server.serve_forever)
    thread.daemon = True
    thread.start()

    return actual_port

def stop_server():
    global _server
    if _server:
        _server.shutdown()
        _server.server_close()
        _server = None
