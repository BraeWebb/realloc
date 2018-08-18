from api.database import *


DATABASE_TABLES = ("user", )


def create_tables(connection):
    pass


if __name__ == "__main__":
    if not database_exists("realloc"):
        create_database("realloc")

    with Database() as connection:
        if not tables_exist(connection, DATABASE_TABLES):
            create_tables(connection)
