import alembic.config
import os
import testing.postgresql
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testing.common.database import DatabaseFactory

from pause import pause, models
from server import app


# Create database tables
def initialize_test_database(postgresql):
    db_port = postgresql.dsn()['port']
    db_host = postgresql.dsn()['host']
    db_user = postgresql.dsn()['user']
    database = postgresql.dsn()['database']
    os.environ['DB_NAME'] = database

    os.environ['DB_CONNECTION'] = ('postgresql://' + db_user + '@' + db_host +
        ':' + str(db_port) + '/' + database)

    models.engine = create_engine(os.environ['DB_CONNECTION'])

    models.Session = sessionmaker(bind=models.engine)

    alembicArgs = [
        '--raiseerr',
        'upgrade', 'head',
    ]

    alembic.config.main(argv=alembicArgs)


# Create factory instance of Postgresql class that has cached database for
# testing
class PostgresqlFactory(DatabaseFactory):
    target_class = testing.postgresql.Postgresql


Postgresql = PostgresqlFactory(cache_initialized_db=True,
                               on_initialized=initialize_test_database)


class PauseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.postgresql = Postgresql()
        self.db_port = self.postgresql.dsn()['port']
        self.db_host = self.postgresql.dsn()['host']
        self.db_user = self.postgresql.dsn()['user']
        self.database = self.postgresql.dsn()['database']

        os.environ['DB_CONNECTION'] = ('postgresql://' + self.db_user + '@' +
            self.db_host + ':' + str(self.db_port) + '/' + self.database)

        models.engine = create_engine(os.environ['DB_CONNECTION'])

        models.Session = sessionmaker(bind=models.engine)

    def tearDown(self):
        self.postgresql.stop()
