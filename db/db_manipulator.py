import psycopg2
from psycopg2 import Error


import datetime
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


def create_update_tsv(connection, cursor):
    """
    creates a function if not exists to automatically tokenize and leximises title and textual
    data on INSERT to database
    """
    create_func = """
    CREATE OR REPLACE FUNCTION update_tsv() RETURNS trigger
        LANGUAGE 'plpgsql' VOLATILE NOT LEAKPROOF
    AS $BODY$
        begin
          new.tsv :=
            setweight(to_tsvector('pg_catalog.english',
              coalesce(new.title,'')), 'A') ||
            setweight(to_tsvector('pg_catalog.english',
              coalesce(new.body,'')), 'D');
         return new;
        end
    $BODY$;
    """
    # Execute a command: this creates a new table
    cursor.execute(create_func)
    connection.commit()
    print("Created automatic text search vector builder function")


def init_tables(connection, cursor):
    """
    Clearing up the table, and recreating them from scratch. Creating tsvector column,
    and indexing by it. Making automatic tsv from textual data on insert
    """
    # Creating asr table:
    create_table_query = """
    DROP TABLE IF EXISTS asr;
    CREATE TABLE asr
    (
        vidos_id INT NOT NULL PRIMARY KEY,
        path TEXT NOT NULL,
        title TEXT NOT NULL,
        client_id INT,
        time_added timestamp NOT NULL,
        body TEXT NOT NULL,
        tsv tsvector NOT NULL
    );
"""
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("\nTable created successfully in PostgreSQL ")

    create_update_tsv(connection, cursor)
    create_index = """
    CREATE INDEX asr_index
        ON asr USING gin (tsv);
    """
    create_tsv_trigger = """
    CREATE TRIGGER update_tsv
       BEFORE INSERT OR UPDATE ON asr
       FOR EACH ROW EXECUTE PROCEDURE update_tsv();
    """
    cursor.execute(create_index)
    cursor.execute(create_tsv_trigger)
    connection.commit()
    print("Successfully created trigger, indexed and automized the creation of tsv!!!\n\n")


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
