import unittest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session

from pyStock.models import Base  # This is your declarative base class
from pyStock.models import *
from pyStock.models.money import *

# Connect to the database and create the schema within a transaction
engine = create_engine('sqlite://')
connection = engine.connect()
transaction = connection.begin()
Base.metadata.create_all(connection)


def teardown_module():
    # Roll back the top level transaction and disconnect from the database
    transaction.rollback()
    connection.close()
    engine.dispose()


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.trans = connection.begin()
        self.session = Session(connection)

    def tearDown(self):
        self.trans.rollback()
        self.session.close()
