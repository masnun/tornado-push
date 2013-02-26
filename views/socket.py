from tornado.websocket import WebSocketHandler
from core.storage import SOCKETS
from database.maindb import Database
import datetime
import json


class ClientSocket(WebSocketHandler):
    def open(self):
        SOCKETS.append(self)
        print "WebSocket opened"

        db = Database()
        messages = db.get_messages(5)

        for msg in messages:
            response = {'user': msg[2], 'action': 'add', 'val': msg[1], 'line': msg[0],
                        'date': str(datetime.datetime.fromtimestamp(msg[3]).strftime("%B %d, %Y"))}
            data = json.dumps(response)
            self.write_message(data)

    def on_close(self):
        print "WebSocket closed"
        SOCKETS.remove(self)


