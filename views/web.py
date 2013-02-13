from core.handlers import WebRequestHandler
from core.socket_storage import SOCKETS
from settings import SECRET_KEY
import hashlib
import time
from database.wordpress import WordPress
import json


class FrontPage(WebRequestHandler):
    def get(self):
        self.render('chat.html', {'host': self.request.host})


class Pusher(WebRequestHandler):
    def get(self, *args, **kwargs):
        data = self.get_argument('data')
        for socket in SOCKETS:
            socket.write_message(data)
        self.write('Posted')


class AuthToken(WebRequestHandler):
    def post(self, *args, **kwargs):
        secret_key = self.get_argument('secret_key', None)
        username = self.get_argument('username', None)
        if secret_key == SECRET_KEY:
            token = hashlib.md5(str(time.time()) + username).hexdigest()
            wp = WordPress()
            wp.set_token(username, token)

            response = {'status': 'ok', 'token': token}
            self.write(json.dumps(response))

        else:
            response = {'status': 'error', 'token': None}
            self.write(json.dumps(response))




