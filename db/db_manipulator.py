import datetime
# from db.db_initialization import init_tables
# from db.connection import connect_to_db, disconnect
# item_purchase_time = datetime.datetime.now()

# To create db on unix:
# su - postgres   OR    sudo -i -u postgres
# psql
# CREATE DATABASE postgres_db;


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


def search_asr(connection, cursor, query):
    search_stmt = """
    SELECT
        ts_rank("tsv", to_tsquery(%s)) AS "rank",
        path,
        title,
        ts_headline(body,
                     to_tsquery(%s),
                     'StartSel=*,StopSel=*,MaxFragments=2,' ||
                     'FragmentDelimiter=...,MaxWords=15,MinWords=1') AS "headline",
        tsv
    FROM
        asr
    WHERE
        tsv @@ to_tsquery(%s)
    ORDER BY rank DESC LIMIT 5;
    """
    cursor.execute(search_stmt, [query, query, query])
    return cursor.fetchall()


# if __name__ == '__main__':
#     connection, cursor = connect_to_db()
#     init_tables(connection, cursor)
#     insert_acs(connection, cursor, 0, "_", "second one",
#                "To start, we will create a file called base.py in the main directory of our project and add the following code to it:")
#     insert_acs(connection, cursor, 2, "_", "first one",
#                "To start, we will create a file called base.py in the main. Our starting position directory of our project and add the following code to it:")
#     for i in search_asr(connection, cursor, "start"):
#         print(i)
#     disconnect(connection, cursor)
