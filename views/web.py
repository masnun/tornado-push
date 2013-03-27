from core.handlers import WebRequestHandler
from core.storage import SOCKETS
from settings import SECRET_KEY
import hashlib
import time
from database.maindb import Database
import json


class FrontPage(WebRequestHandler):
    def get(self):
        token = self.get_argument('csrf_token', None)
        db = Database()
        user, mod = db.get_username(token)
        self.render('chat.html', {'host': self.request.host, 'csrf_token': token, 'mod': mod})


class Pusher(WebRequestHandler):
    def post(self, *args, **kwargs):
        value = self.get_argument('val', None)
        action = self.get_argument('action', None)
        csrf_token = self.get_argument('csrf_token', None)

        # Sanitize Input
        if value is not None:
            restricted_words = ['<script>', '<p>', '</p>']
            for x in restricted_words:
                value = value.replace(x, '')

        if value == '':
            value = None

        if value is not None and action is not None and csrf_token is not None:
            db = Database()
            user, mod = db.get_username(csrf_token)

            if user is not None:
                # Add message
                if action == 'add':
                    for socket in SOCKETS:
                        line_id, date = db.save_message(user, value)
                        response = {'user': user, 'action': action, 'val': value, 'line': line_id,
                                    'online': len(SOCKETS)}
                        data = json.dumps(response)
                        socket.write_message(data)
                    self.write('Added')

                #Remove message
                if action == 'remove':
                    response = {'user': user, 'action': action, 'val': value, 'online': len(SOCKETS)}
                    data = json.dumps(response)
                    if int(mod) == 1:
                        for socket in SOCKETS:
                            db.remove_message(value)
                            socket.write_message(data)
                        self.write('Remove command issued')
                    else:
                        self.write('Permission denied')

                # Remove all messages
                if action == 'remove_all':
                    response = {'user': user, 'action': action, 'val': value, 'online': len(SOCKETS)}
                    data = json.dumps(response)
                    if int(mod) == 1:
                        for socket in SOCKETS:
                            db.remove_all_messages(value)
                            socket.write_message(data)
                        self.write('Removed all messages')
                    else:
                        self.write('Permission denied')


            else:
                self.write('Invalid Value')
        else:
            self.write('No user found')


class AuthToken(WebRequestHandler):
    def post(self, *args, **kwargs):
        secret_key = self.get_argument('secret_key', None)
        username = self.get_argument('username', None)
        mod = self.get_argument('mod', 0)

        if secret_key == SECRET_KEY:
            token = hashlib.md5(str(time.time()) + username).hexdigest()
            db = Database()
            db.set_token(username, token, int(mod))

            response = {'status': 'ok', 'token': token}
            self.write(json.dumps(response))

        else:
            response = {'status': 'error', 'token': None}
            self.write(json.dumps(response))
