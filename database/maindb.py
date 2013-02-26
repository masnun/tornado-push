from database.core import connect_db
import time, datetime


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
        cursor = self.db_connection.cursor()
        time_stamp = int(time.time())
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
