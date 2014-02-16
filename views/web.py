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

        print self.request.host

        if user:
            self.render('chat.html', {'host': self.request.host, 'user': user, 'csrf_token': token, 'mod': mod})
        else:
            self.write("User could not be verified <br/>")
            if token == 'banned':
                self.write('You are banned!')


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
            user_id = db.get_user_id(csrf_token)

            if user is not None and not db.is_banned(user):
                # Add message
                if action == 'add':
                    line_id, date = db.save_message(user, value)
                    db.add_karma_points("Added message", 1, user_id)
                    response = {'user': user, 'action': action, 'val': value, 'line': line_id,
                                'online': len(SOCKETS)}
                    data = json.dumps(response)

                    for socket in SOCKETS:
                        socket.write_message(data)
                    self.write('Added')


                # Add private message
                if action == 'pvt_msg':
                    username = self.get_argument('username', None)
                    line_id, date = db.save_pvt_message(user, username, value)
                    response = {'user': user, 'action': action, 'val': value, 'username': username, 'line': line_id,
                                'online': len(SOCKETS)}
                    data = json.dumps(response)
                    for socket in SOCKETS:
                        socket.write_message(data)
                    self.write('Added')

                #Remove message
                if action == 'remove':
                    response = {'user': user, 'action': action, 'val': value, 'online': len(SOCKETS)}
                    data = json.dumps(response)
                    if int(mod) == 1:
                        db.remove_message(value)
                        for socket in SOCKETS:
                            socket.write_message(data)
                        self.write('Remove command issued')
                    else:
                        self.write('Permission denied')

                # Remove all messages
                if action == 'remove_all':
                    response = {'user': user, 'action': action, 'val': value, 'online': len(SOCKETS)}
                    data = json.dumps(response)
                    if int(mod) == 1:
                        db.remove_all_messages(value)
                        for socket in SOCKETS:
                            socket.write_message(data)
                        self.write('Removed all messages')
                    else:
                        self.write('Permission denied')

                # Ban user
                if action == 'ban':
                    response = {'user': user, 'action': action, 'val': value, 'online': len(SOCKETS)}
                    data = json.dumps(response)
                    if int(mod) == 1:
                        db.ban_user(value)
                        for socket in SOCKETS:
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
        userid = self.get_argument('user_id', None)
        mod = self.get_argument('mod', 0)
        db = Database()

        if db.is_banned(username):
            response = {'status': 'ok', 'token': 'banned'}
            self.write(json.dumps(response))
        else:
            if secret_key == SECRET_KEY:
                token = hashlib.md5(str(time.time()) + username).hexdigest()

                db.set_token(username, int(userid), token, int(mod))

                response = {'status': 'ok', 'token': token}
                self.write(json.dumps(response))

            else:
                response = {'status': 'error', 'token': None}
                self.write(json.dumps(response))

class BanManager(WebRequestHandler):
    def get(self):
        token = self.get_argument('csrf_token', None)
        db = Database()
        user, mod = db.get_username(token)
        rm = self.get_argument('rm', None)

        if mod and rm is not None:
            db.remove_banned_user(rm)

        if mod:
            bans = db.get_banned_users()
            self.render('bans.html',{'bans': bans, 'token': token})
        else:
            self.write("You are not a moderator!")