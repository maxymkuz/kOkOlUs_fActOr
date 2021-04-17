import psycopg2
from psycopg2 import Error

import datetime
from db_initialization import init_tables
# item_purchase_time = datetime.datetime.now()

# To create db on unix:
# su - postgres   OR    sudo -i -u postgres
# psql
# CREATE DATABASE postgres_db;


def connect_to_db(user="postgres",
                  password="postgres",
                  host="127.0.0.1",
                  port="5432",
                  database="postgres_db"):
    """
    :return: connection, cursor
    """
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")

        cursor.execute("SELECT version();")

        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        return connection, cursor

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None


def insert_acs(connection, cursor, vidos_id, path, title, body, client_id=0):
    insrt_stmt = """
    INSERT INTO asr 
        (vidos_id, path, title, client_id, time_added, body)
    VALUES
        (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insrt_stmt, [vidos_id, path, title, client_id,
                                datetime.datetime.now(), body])
    connection.commit()


def search(connection, cursor, query):
    search_stmt = """
    SELECT
        ts_rank("tsv", to_tsquery(%s)) AS "rank",
        path,
        title,
        ts_headline(body,
                     to_tsquery(%s),
                     'StartSel=*,StopSel=*,MaxFragments=2,' ||
                     'FragmentDelimiter=...,MaxWords=15,MinWords=1') AS "headline"
    FROM
        asr
    WHERE
        tsv @@ to_tsquery(%s)
    ORDER BY rank DESC LIMIT 20;
    """
    cursor.execute(search_stmt, [query, query, query])
    return cursor.fetchall()


def disconnect(connection, cursor):
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


if __name__ == '__main__':
    connection, cursor = connect_to_db()
    init_tables(connection, cursor)
    insert_acs(connection, cursor, 0, "_", "second one",
               "To start, we will create a file called base.py in the main directory of our project and add the following code to it:")
    insert_acs(connection, cursor, 2, "_", "first one",
               "To start, we will create a file called base.py in the main. Our starting position directory of our project and add the following code to it:")
    for i in search(connection, cursor, "start"):
        print(i)
    disconnect(connection, cursor)
