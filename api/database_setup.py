from database import *

DATABASE_TABLES = ("user", "course", "session", "availability")
DATABASE_RELATIONS = ("allocation", "course_association")


def create_tables(connection):
    # create user table
    with Database() as connection:
        connection.query("""CREATE TABLE "user" (
                            id bigint NOT NULL,
                            email text NOT NULL,
                            password text NOT NULL,
                            permission integer NOT NULL);""")
    # create course table
    with Database() as connection:
        connection.query("""CREATE TABLE course (
                            id bigint NOT NULL,
                            name text NOT NULL);""")
    # create session table
    with Database() as connection:
        connection.query("""CREATE TABLE "session" (
                            id bigint NOT NULL,
                            course_id bigint NOT NULL,
                            start time NOT NULL,
                            "end" time NOT NULL,
                            "day" text NOT NULL,
                            location text);""")
    # create availability table
    with Database() as connection:
        connection.query("""CREATE TABLE availability (
                            user_id bigint NOT NULL,
                            "day" text NOT NULL,
                            start time NOT NULL,
                            "type" integer NOT NULL);""")


def create_relations(connection):
    with Database() as connection:
        connection.query("""CREATE TABLE allocation (
                            user_id bigint NOT NULL,
                            course_id bigint NOT NULL,
                            session_id bigint NOT NULL,
                            revision integer NOT NULL);""")
    with Database() as connection:
        connection.query("""CREATE TABLE course_association (
                            user_id bigint NOT NULL,
                            course_id bigint NOT NULL);""")


if __name__ == "__main__":
    if not database_exists("realloc"):
        create_database("realloc")

    with Database() as connection:
        if not tables_exist(connection, DATABASE_TABLES):
            create_tables(connection)
        if not tables_exist(connection, DATABASE_RELATIONS):
            create_relations(connection)
