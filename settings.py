import os

TEMPLATE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/templates/"

DATABASE_CONFIGS = {
    'wordpress': {
        'host': 'localhost',
        'database': 'wp_tornado',
        'username': 'root',
        'password': 'masnun'
    }
}

SECRET_KEY = "secret"