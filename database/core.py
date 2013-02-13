import MySQLdb
from settings import DATABASE_CONFIGS


def connect_db(db_name):
    if DATABASE_CONFIGS.has_key(db_name):
        configs = DATABASE_CONFIGS[db_name]
        connection = None
        try:
            connection = MySQLdb.connect(
                host=configs['host'],
                user=configs['username'],
                passwd=configs['password'],
                db=configs['database']
            )
        except Exception, ex:
            print ex.args[1]

        return connection
    else:
        print "The database connection could not be found"
