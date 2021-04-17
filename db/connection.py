import psycopg2
from psycopg2 import Error


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


def disconnect(connection, cursor):
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
