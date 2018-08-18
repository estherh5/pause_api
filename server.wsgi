import os
import sys


sys.path.insert(0, '/var/www/html/pause_api')  # Server path


def application(environ, start_response):
    os.environ['ENV_TYPE'] = environ.get('ENV_TYPE', '')
    os.environ['DB_CONNECTION'] = environ.get('DB_CONNECTION', '')
    os.environ['DB_NAME'] = environ.get('DB_NAME', '')
    from server import app as _application

    return _application(environ, start_response)
