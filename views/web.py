from core.handlers import WebRequestHandler
from core.socket_storage import SOCKETS


class FrontPage(WebRequestHandler):
    def get(self):
        self.render('chat.html', {'host': self.request.host})


class Pusher(WebRequestHandler):
    def get(self, *args, **kwargs):
        data = self.get_argument('data')
        for socket in SOCKETS:
            socket.write_message(data)
        self.write('Posted')