from tornado.websocket import WebSocketHandler
from core.socket_storage import SOCKETS

class ClientSocket(WebSocketHandler):
    def open(self):
        SOCKETS.append(self)
        print "WebSocket opened"

    def on_close(self):
        print "WebSocket closed"
        SOCKETS.remove(self)


