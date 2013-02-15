from core.handlers import WebRequestHandler
from core.storage import SOCKETS, CHAT
from settings import SECRET_KEY
import hashlib
import time
from database.wordpress import WordPress
import json


class FrontPage(WebRequestHandler):
    def get(self):
        user = self.get_argument('user', None)
        if user is None:
            user = 'masnun'
        wp = WordPress()
        token = wp.get_token(user)
        user, mod = wp.get_username(token)
        self.render('chat.html', {'host': self.request.host, 'csrf_token': token, 'mod': mod})


class Pusher(WebRequestHandler):
    def post(self, *args, **kwargs):
        value = self.get_argument('val', None)
        action = self.get_argument('action', None)
        csrf_token = self.get_argument('csrf_token', None)

        if value is not None and action is not None and csrf_token is not None:
            wp = WordPress()
            user, mod = wp.get_username(csrf_token)
            response = {'user': user, 'action': action, 'val': value, 'line': CHAT['line']}
            data = json.dumps(response)

            if action == 'add':
                for socket in SOCKETS:
                    socket.write_message(data)

                newline = CHAT['line'] + 1
                CHAT['line'] = newline
                self.write('Added')

            if action == 'remove':
                if int(mod) == 1:
                    for socket in SOCKETS:
                        socket.write_message(data)
                    self.write('Remove command issued')
                else:
                    self.write('Permission denied')
        else:
            self.write('Invalid Value')


class AuthToken(WebRequestHandler):
    def post(self, *args, **kwargs):
        secret_key = self.get_argument('secret_key', None)
        username = self.get_argument('username', None)
        mod = self.get_argument('mod', 0)

        if secret_key == SECRET_KEY:
            token = hashlib.md5(str(time.time()) + username).hexdigest()
            wp = WordPress()
            wp.set_token(username, token, int(mod))

            response = {'status': 'ok', 'token': token}
            self.write(json.dumps(response))

        else:
            response = {'status': 'error', 'token': None}
            self.write(json.dumps(response))
