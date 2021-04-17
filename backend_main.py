from db.connection import connect_to_db, disconnect
from db.db_manipulator import search_db, insert_db
from db.db_initialization import init_table_asr, init_table_ocr


def find_db(connection, cursor, query, db="asr"):
    """
    Query: has to be of
    """
    db_ans = search_db(connection, cursor, query, db=db)
    for video in db_ans:
        print(video)

        tsv = video[-1]
        print(tsv)
        dictionary = {k.replace("'", ""): v for k, v in [part.split(":") for part in
                                                            tsv.split()]}
        print(type(dictionary), dictionary)


def main():
    connection, cursor = connect_to_db()
    init_table_asr(connection, cursor)
    init_table_ocr(connection, cursor)

    text1 = "To start, we will create a file called base.py in the main directory of our project and add the following code to it:"
    text2 = "To start, we will create a file called base.py in the main. Our starting position directory of our project and add the following code to it:"

    insert_db(connection, cursor, 0, "_", "second title one",
              text1.split(), ["RAndom_timestamp" for _ in range(len(text1.split()))], db="ocr")
    insert_db(connection, cursor, 1, "_", "first title one",
              text2.split(), ["RAndom_timestamp" for i in range(len(text2.split()))], db="ocr")
    print()
    find_db(connection, cursor, "StarTinG", db="ocr")


if __name__ == '__main__':
    main()
