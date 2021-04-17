import datetime
from psycopg2 import sql


# from db.db_initialization import init_tables
# from db.connection import connect_to_db, disconnect
# item_purchase_time = datetime.datetime.now()

# To create db on unix:
# su - postgres   OR    sudo -i -u postgres
# psql
# CREATE DATABASE postgres_db;


def insert_db(connection, cursor, vidos_id, path, title, words_lst, timestamp_lst, db="asr",
              client_id=0):
    """
    Прочитай уважно шо подається

    :param db: "asr" or "ocr"
    :param vidos_id: УНІКАЛЬНИЙ ДЛЯ КОЖНОГО ВІДОСУ, ЗАДАЄТЬСЯ ВРУЧНУ
    :param path: то має бути юрлка на ютуб напирклад
    :param title: посплітена назва відосу як я в тг вчора писав
    :param words_lst:        ["word1", "word2", "word3", "word4"]
    :param timestamp_lst:    ["timestamp1", "timestamp2", "timestamp3", "timestamp4"]
    :param client_id:    забий хуй і нич не передавай
    :return:
    """
    insrt_stmt = """
    INSERT INTO {} 
        (vidos_id, path, title, client_id, time_added, body, timestamps, text_as_array)
    VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql.SQL(insrt_stmt).format(sql.Identifier(db)),
                       [
                           vidos_id, path, title, client_id,
                           datetime.datetime.now(), " ".join(words_lst),
                           timestamp_lst, words_lst
                       ])
        connection.commit()
        print(f"Successfully added {title} to the DB!")
    except:
        print(f"Was not able to insert video {title}, Probably wrong input")


def search_db(connection, cursor, query, db="asr", language="'english'"):
    search_stmt = f"""
    SELECT
        ts_rank("tsv", to_tsquery({language}, %s)) AS "rank",
        path,
        title,
        ts_headline(body,
                     to_tsquery({language}, %s),
                     'StartSel=*,StopSel=*,MaxFragments=2,' ||
                     'FragmentDelimiter=...,MaxWords=15,MinWords=1') AS "headline",
        timestamps,
        text_as_array,
        tsv
    FROM
        {{}}
    WHERE
        tsv @@ to_tsquery({language}, %s)
    ORDER BY rank DESC LIMIT 5;
    """
    cursor.execute(sql.SQL(search_stmt).format(sql.Identifier(db)),
                   [query, query, query])
    return cursor.fetchall()

# if __name__ == '__main__':
#     connection, cursor = connect_to_db()
#     for i in search_asr(connection, cursor, "start"):
#         print(i)
#     disconnect(connection, cursor)
