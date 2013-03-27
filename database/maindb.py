from database.core import connect_db
import time
import datetime


class Database:
    def __init__(self):
        self.db_connection = connect_db('wordpress')

    def get_connection(self):
        return self.db_connection

    def set_token(self, username, token, mod=0):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_name='" + str(username) + "'")
        cursor.execute(
            "INSERT INTO users (user_name,csrf_token,`mod`) VALUES ('" + str(username) + "','" + str(
                token) + "','" + str(mod) + "') ")
        self.db_connection.commit()

    def get_token(self, username):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM users WHERE user_name='" + str(username) + "'"
        cursor.execute(query)
        data = cursor.fetchone()

        return data[1]

    def get_username(self, token):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM users WHERE csrf_token='" + str(token) + "'"
        cursor.execute(query)
        data = cursor.fetchone()

        if data is not None:
            return data[0], data[2]
        else:
            return None, None

    def save_message(self, user_name, message):
        if self.is_banned(user_name):
            return False, False
        else:
            cursor = self.db_connection.cursor()
            time_stamp = int(time.time())
            message = self.db_connection.escape_string(message)
            query = "INSERT INTO messages (user_name,message,time_stamp) VALUES ('" + user_name + "','" + message + "'," + str(
                time_stamp) + ")"

            cursor.execute(query)
            line_id = self.db_connection.insert_id()
            self.db_connection.commit()
            return line_id, str(datetime.datetime.fromtimestamp(time_stamp).strftime("%B %d, %Y"))

    def remove_message(self, message_id):
        cursor = self.db_connection.cursor()
        query = "DELETE FROM messages WHERE id=" + str(message_id)
        cursor.execute(query)
        self.db_connection.commit()

    def get_messages(self, number):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM messages ORDER BY id DESC LIMIT 0," + str(number)
        cursor.execute(query)
        data = cursor.fetchall()
        messages = []
        for x in data:
            messages.append(x)

        messages.reverse()
        return messages

    def remove_all_messages(self, username):
        cursor = self.db_connection.cursor()
        query = "DELETE FROM messages WHERE user_name='" + str(username) + "'"
        cursor.execute(query)
        self.db_connection.commit()

    def ban_user(self, username):
        cursor = self.db_connection.cursor()
        username = self.db_connection.escape_string(username)
        query = "INSERT INTO banned_users (username) VALUES ('" + username + "')"
        cursor.execute(query)
        self.db_connection.commit()


    def is_banned(self, username):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM users WHERE user_name='" + str(
            username) + "' and user_name in (SELECT username FROM banned_users)"
        cursor.execute(query)
        data = cursor.fetchall()

        if len(data) > 0:
            return True
        else:
            return False

