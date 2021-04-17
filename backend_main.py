from db.connection import connect_to_db, disconnect
from db.db_manipulator import search_db, insert_db
from db.db_initialization import init_table_asr, init_table_ocr
from db.tokenizer import tokenize_word
from backend.write_to_db import json_to_db


def tokenize_full_text(connection, cursor, array):
    for i in range(len(array)):
        array[i] = tokenize_word(connection, cursor, array[i])
    return array


def find_db(connection, cursor, query, db="asr"):
    """
    Query: has to be of
    """
    query = query.split()
    query_for_db = "&".join(query)
    db_ans = search_db(connection, cursor, query_for_db, db=db)

    ranked_videos = []

    for ranked_video in db_ans:
        # print(ranked_video)

        tokenized_text = tokenize_full_text(connection, cursor, ranked_video[-2])
        timestamps = ranked_video[-3]
        rank = ranked_video[0]
        url = ranked_video[1]
        title = ranked_video[2]

        # print(rank, title, url, timestamps)
        # print(tokenized_text)

        # searching through tokenized_words:
        result_dict = dict()
        for word in query:
            word = tokenize_word(connection, cursor, word)
            # print(word)
            result_dict[word] = []
            for i in range(len(tokenized_text)):
                if tokenized_text[i] == word:
                    result_dict[word].append(timestamps[i])
        ranked_videos.append([rank, url, title, result_dict])

        print(result_dict)

        # dictionary = {k.replace("'", ""): v for k, v in [part.split(":") for part in
        #                                                  tsv.split()]}
    return ranked_videos


def add_to_db():
    connection, cursor = connect_to_db()
    init_table_asr(connection, cursor)
    init_table_ocr(connection, cursor)
    json_to_db(connection, cursor, insert_db, "./backend/ocr.json", db="ocr")
    json_to_db(connection, cursor, insert_db, "./backend/asr.json", db="asr")
    return connection, cursor


def main():
    connection, cursor = add_to_db()

    search_result = find_db(connection, cursor, "binary search", db="asr")
    print(search_result)


if __name__ == '__main__':
    main()
