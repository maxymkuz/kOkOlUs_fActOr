import datetime


# from db.db_initialization import init_tables
# from db.connection import connect_to_db, disconnect
# item_purchase_time = datetime.datetime.now()

# To create db on unix:
# su - postgres   OR    sudo -i -u postgres
# psql
# CREATE DATABASE postgres_db;


def insert_acs(connection, cursor, vidos_id, path, title, words_lst, timestamp_lst, client_id=0):
    """
    Прочитай уважно шо подається

    :param vidos_id: УНІКАЛЬНИЙ ДЛЯ КОЖНОГО ВІДОСУ, ЗАДАЄТЬСЯ ВРУЧНУ
    :param path: то має бути юрлка на ютуб напирклад
    :param title: посплітена назва відосу як я в тг вчора писав
    :param words_lst:        ["word1", "word2", "word3", "word4"]
    :param timestamp_lst:    ["timestamp1", "timestamp2", "timestamp3", "timestamp4"]
    :param client_id:    забий хуй і нич не передавай
    :return:
    """
    insrt_stmt = """
    INSERT INTO asr 
        (vidos_id, path, title, client_id, time_added, body, timestamps, text_as_array)
    VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(insrt_stmt, [vidos_id, path, title, client_id,
                                    datetime.datetime.now(), " ".join(words_lst),
                                    timestamp_lst, words_lst
                                    ])
        connection.commit()
        print(f"Successfully added {title} to the DB!")

    except:
        print(f"Was not able to insert video {title}, Probably wrong input")


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
        timestamps,
        text_as_array,
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
#     for i in search_asr(connection, cursor, "start"):
#         print(i)
#     disconnect(connection, cursor)
