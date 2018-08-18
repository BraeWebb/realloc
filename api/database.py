import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

HOST = None
USER = None
PASSWORD = None
DATABASE = None
try:
    import config
    HOST = config.host
    USER = config.user
    PASSWORD = config.password
    DATABASE = config.database
except ImportError:
    pass


class Database:
    """
    A database connection that handles automatic commit and rollback
    with a context manager.
    """

    def __init__(self, host=HOST, user=USER, password=PASSWORD, database=DATABASE):
        """Establish a connection to the database and initialize the class"""
        self.db = psycopg2.connect(host=host, user=user, password=password,
                                   database=database)
        self.cursor = self.db.cursor()

    def commit(self):
        """Commit the queries previously run on the database"""
        self.db.commit()

    def rollback(self):
        """Rollback the queries previously run on the database"""
        self.db.rollback()

    def close(self):
        """Close the cursor object and the connection to the database

        Used when closing the context manager or deleting the object
        """
        self.cursor.close()
        self.db.close()

    def __enter__(self):
        """Allows for the database to have context management"""
        return self

    def __exit__(self, exception_type, exception_val, trace):
        """If an error occurred rollback the database, otherwise, commits

        Allows for the database to have context management
        """
        if not exception_type:
            self.commit()
        else:
            self.rollback()
        self.close()

    def query(self, query, *variables, limit=None):
        """Execute a SQL query on the database.

        An SQL string can have variables, denoted by %s which should be passed
        as extra parameters to this method.

        Parameters:
            query (str): an SQL statement to execute on the database
            *variables (str): the items to place in the query in the place of %s
            limit (int): the maximum amount of rows to fetch

        Returns:
            (tuple<tuple<*>>): Rows with data from the query. None if error.
        """
        self.cursor.execute(query, variables)
        try:
            if limit:
                return self.cursor.fetchmany(limit)
            else:
                return self.cursor.fetchall()
        except psycopg2.ProgrammingError:
            return None

    def exists(self, table, **where):
        """Check if rows exist in a table satisfying the given where clauses.

        Parameters:
            table (str): the database table to check.
            **where (dict<str, *>, optional): where conditions for searching rows.

        Returns:
            (bool): Whether a row with the where conditions is found.
        """
        # Format the list of where statements
        wheres = ' AND '.join([str(attr) + '=\'' + str(val) + '\'' for attr, val in where.items()])

        if where:
            query = 'SELECT COUNT(*) FROM {} WHERE {}'.format(table, wheres)
        else:
            query = 'SELECT COUNT(*) FROM {}'.format(table, wheres)
        self.cursor.execute(query)

        return bool(self.cursor.fetchone()[0])

    def __bool__(self):
        """Return true if the database has an open connection, false otherwise"""
        return not bool(self.db.closed)


def create_database(database):
    """Create a new database with a given database name."""
    # open an existing postgres database
    with Database(database="postgres") as connection:
        # set isolation level (dunno why tbqh)
        connection.db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        connection.query("CREATE DATABASE " + database)


def tables_exist(connection, tables):
    """Ensure that all the given tables exist"""
    for table in tables:
        try:
            connection.exists(table)
        except psycopg2.ProgrammingError:
            return False
    return True


def database_exists(database):
    """Ensure that a database exists"""
    try:
        test_connection_db = Database(database=database)
        test_connection_db.close()
        return True
    except psycopg2.OperationalError:
        return False
