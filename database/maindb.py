from database.core import connect_db
import time
import datetime


class Database:
    def __init__(self):
        self.db_connection = connect_db('wordpress')

    def get_connection(self):
        return self.db_connection

    def set_token(self, username, user_id, token, mod=0):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_name='" + str(username) + "'")
        cursor.execute(
            "INSERT INTO users (user_name, user_id, csrf_token,`mod`) VALUES ('"
            + str(username) + "'," + str(user_id) + ",'" + str(token) + "','" + str(mod) + "') ")
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
            return data[0], data[3]
        else:
            return None, None

    def get_user_id(self, token):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM users WHERE csrf_token='" + str(token) + "'"
        cursor.execute(query)
        data = cursor.fetchone()

        if data is not None:
            return data[1]
        else:
            return None

    def get_user_id_from_username(self, username):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM users WHERE user_name='" + str(username) + "'"
        cursor.execute(query)
        data = cursor.fetchone()

        if data is not None:
            return data[1]
        else:
            return None


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

    def save_pvt_message(self, user_name, to_user, message):
        if self.is_banned(user_name):
            return False, False
        else:
            cursor = self.db_connection.cursor()
            timestamp = int(time.time())
            message = self.db_connection.escape_string(message)
            query = "INSERT INTO private_messages (username,message,to_user,timestamp) VALUES ('" + user_name + "','" + message + "','" + to_user + "'," + str(
                timestamp) + ")"

            cursor.execute(query)
            line_id = self.db_connection.insert_id()
            self.db_connection.commit()
            return line_id, str(datetime.datetime.fromtimestamp(timestamp).strftime("%B %d, %Y"))

    def remove_message(self, message_id):

        #Handle Karma
        message = self.get_message(message_id)
        username = message[2]
        user_id = self.get_user_id_from_username(username)
        self.add_karma_points("One message removed", -5, user_id)

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

    def get_message(self, id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM messages WHERE id=" + str(id)
        cursor.execute(query)
        data = cursor.fetchall()
        return data[0]


    def remove_all_messages(self, username):
        #Handle Karma
        user_id = self.get_user_id_from_username(username)
        self.add_karma_points("All messages removed", -50, user_id)

        cursor = self.db_connection.cursor()
        query = "DELETE FROM messages WHERE user_name='" + str(username) + "'"
        cursor.execute(query)
        self.db_connection.commit()

    def ban_user(self, username, message="N/A"):
        #Handle Karma
        user_id = self.get_user_id_from_username(username)
        self.add_karma_points("User banned: " + message, -500, user_id)

        cursor = self.db_connection.cursor()
        username = self.db_connection.escape_string(username)
        query = "INSERT INTO banned_users (username, message) VALUES ('" + username + "','" + message + "')"
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

    def get_banned_users(self):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM banned_users"
        cursor.execute(query)
        data = cursor.fetchall()

        return data

    def remove_banned_user(self, username):
        cursor = self.db_connection.cursor()
        query = "DELETE FROM banned_users WHERE username='" + str(username) + "'"
        cursor.execute(query)
        self.db_connection.commit()


    def add_karma_points(self, description, points, user_id):
        cursor = self.db_connection.cursor()
        p_date = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO wp_karma_points (points_desc, points, user_id, p_date) VALUES ('" + description + "'," + str(
            points) + "," + str(user_id) + ",'" + p_date + "')"

        cursor.execute(query)
        line_id = self.db_connection.insert_id()
        self.db_connection.commit()
        return line_id

    def get_likes_dislikes_message(self, message_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM likes_dislikes WHERE message_id=" + str(message_id)
        cursor.execute(query)
        data = cursor.fetchall()

        if data:
            return data
        else:
            query = "INSERT INTO likes_dislikes (message_id, likes, dislikes) VALUES (" + str(message_id) + ",0,0)"
            cursor.execute(query)
            line_id = self.db_connection.insert_id()
            self.db_connection.commit()

            return message_id, 0, 0,

    def update_likes_dislikes_message(self, message_id, col, value):
        cursor = self.db_connection.cursor()
        query = "UPDATE likes_dislikes SET " + str(col) + "='" + str(value) + "' where message_id=" + str(message_id)
        cursor.execute(query)


    def update_likes_for_message(self, message_id):
        likes = self.get_likes_dislikes_message(message_id)[1]

