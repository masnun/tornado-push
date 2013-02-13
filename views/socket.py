from tornado.websocket import WebSocketHandler
from core.storage import SOCKETS

class ClientSocket(WebSocketHandler):
    def open(self):
        SOCKETS.append(self)
        print "WebSocket opened"

    def on_close(self):
        print "WebSocket closed"
        SOCKETS.remove(self)


