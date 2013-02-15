from database.core import connect_db


class WordPress:
    def __init__(self):
        self.db_connection = connect_db('wordpress')

    def get_connection(self):
        return self.db_connection

    def set_token(self, username, token, mod=0):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_name='" + username + "'")
        cursor.execute(
            "INSERT INTO users (user_name,csrf_token,mod) VALUES ('" + username + "','" + token + "','" + mod + "') ")
        self.db_connection.commit()


    def get_token(self, username):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM users WHERE user_name='" + username + "'"
        cursor.execute(query)
        data = cursor.fetchone()

        return data[1]

    def get_username(self, token):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM users WHERE csrf_token='" + token + "'"
        cursor.execute(query)
        data = cursor.fetchone()

        return data[0], data[2]