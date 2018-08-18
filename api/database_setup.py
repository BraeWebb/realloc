from api.database import *


DATABASE_TABLES = ("user", "course", "session", "availability")
DATABASE_RELATIONS = ("allocation", "course_association")


def create_tables(connection):
    # create user table
    connection.query("""CREATE TABLE "user" (
                        id integer NOT NULL PRIMARY KEY,
                        email text NOT NULL,
                        password text NOT NULL,
                        permission integer NOT NULL);""")
    # create course table
    connection.query("""CREATE TABLE course (
                        id integer NOT NULL PRIMARY KEY,
                        name text NOT NULL);""")
    # create session table
    connection.query("""CREATE TABLE "session" (
                        id integer NOT NULL PRIMARY KEY,
                        course_id integer NOT NULL PRIMARY KEY,
                        start time NOT NULL,
                        "end" time NOT NULL,
                        "day" date NOT NULL,
                        location text);""")
    # create availability table
    connection.query("""CREATE TABLE availability (
                        user_id integer NOT NULL,
                        "day" date NOT NULL,
                        start time NOT NULL,
                        end time);""")


def create_relations(connection):
    connection.query("""CREATE TABLE allocation (
                        user_id integer NOT NULL PRIMARY KEY,
                        course_id integer NOT NULL PRIMARY KEY,
                        session_id integer NOT NULL PRIMARY KEY,
                        revision integer NOT NULL PRIMARY KEY);""")

    connection.query("""CREATE TABLE course_association (
                        user_id integer NOT NULL PRIMARY KEY,
                        course_id integer NOT NULL PRIMARY KEY);""")


if __name__ == "__main__":
    if not database_exists("realloc"):
        create_database("realloc")

    with Database() as connection:
        if not tables_exist(connection, DATABASE_TABLES):
            create_tables(connection)
        if not tables_exist(connection, DATABASE_RELATIONS):
            create_relations(connection)
