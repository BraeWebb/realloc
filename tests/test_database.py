import os
import sys
import unittest

from psycopg2 import InterfaceError

sys.path.insert(0, os.path.abspath('..'))
from api.database import Database

TEST_DATABASE = "test_database"


class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Create/Wipe a table called test_data where tests will be run"""
        self.connection = Database(database=TEST_DATABASE)

    def tearDown(self):
        """Drop the test_data table used to perform tests"""
        self.connection.close()

    def test_commit(self):
        """Ensure that the database commit method retains
        the data after reconnection.
        """
        # insert test data and commit
        self.connection.query('INSERT INTO test_data (variable) VALUES (1)')
        self.connection.commit()
        self.connection.close()

        # reopen connection and query to ensure data was retained
        self.connection = Database(database=TEST_DATABASE)
        result = self.connection.query('SELECT * FROM test_data')
        self.assertEqual(result, [(1,)])

    def test_rollback(self):
        """Ensure that the database rollback method removes changes to the data
        """
        # insert test data and rollback
        self.connection.query('INSERT INTO test_data (variable) VALUES (1)')
        self.connection.rollback()
        self.connection.close()

        # reopen connection and query to ensure data was removed
        self.connection = Database(database=TEST_DATABASE)
        result = self.connection.query('SELECT * FROM test_data')
        self.assertEqual(result, [])

    def test_close(self):
        """Ensure that the close method closes the database connection"""
        with self.assertRaises(InterfaceError):
            self.connection.close()
            self.connection.query('SELECT * FROM test_data')

    def test_with_commit(self):
        """Ensure that an error free with statement commits when exiting

        Performs an error free with block and ensures the data remains
        """
        with Database(database=TEST_DATABASE) as db:
            db.query('INSERT INTO test_data (variable) VALUES (1)')
        result = self.connection.query('SELECT * FROM test_data')
        self.assertEqual(result, [(1,)])

    def test_with_rollback(self):
        """Ensure that an error occurring in a database with context forces the database to rollback

        Raises an error in the with context and ensures that modifications were removed
        """
        try:
            with Database(database=TEST_DATABASE) as db:
                db.query('INSERT INTO test_data (variable) VALUES (1)')
                raise Exception
        except:
            pass
        result = self.connection.query('SELECT * FROM test_data')
        self.assertEqual(result, [])

    def test_limit(self):
        """Ensure that the limit keyword of the query method works as expected

        Performs several queries with varying limits and compares the results to the expected results
        """
        self.connection.query('INSERT INTO test_data (variable) VALUES (1), (2), (3), (4), (5)')

        result = self.connection.query('SELECT * FROM test_data', limit=1)
        self.assertEqual(result, [(1,)])

        result = self.connection.query('SELECT * FROM test_data', limit=3)
        self.assertEqual(result, [(1,), (2,), (3,)])

        result = self.connection.query('SELECT * FROM test_data')
        self.assertEqual(result, [(1,), (2,), (3,), (4,), (5,)])

    def test_exists(self):
        """Ensure that the exists method accurately reports the existence of rows in the database"""
        self.connection.query('INSERT INTO test_data (variable) VALUES (1), (2), (3), (4), (5)')

        self.assertTrue(self.connection.exists('test_data'))
        self.assertTrue(self.connection.exists('test_data', variable=3))
        self.assertFalse(self.connection.exists('test_data', variable=6))

    def test_bool(self):
        """Ensure that the database returns the correct boolean value based on whether it is open or closed"""
        self.assertTrue(self.connection)
        self.connection.close()
        self.assertFalse(self.connection)

    def test_del(self):
        """Ensure that the __del__ magic method works in the same way the close works"""
        with self.assertRaises(InterfaceError):
            self.connection.__del__()
            self.connection.query('SELECT * FROM test_data')


if __name__ == '__main__':
    unittest.main()
