import json


def json_to_db(connection, cursor, insert_func, path_to_json, db="asr"):
    with open(path_to_json) as json_file:
        data = json.load(json_file)
        for id in data:
            video = data[id]
            title = video["title"]
            words_lst = video["words_lst"]
            timestamp_lst = video["timestamp_lst"]
            insert_func(connection, cursor, id, title,
                      words_lst, timestamp_lst, db=db)

            # print(video)

    # text1 = "To start, we will create a file called base.py in the main directory of our project and add the following code to it:"
    # insert_db(connection, cursor, 0, "_", "second title one",
    #           text1.split(), ["RAndom_timestamp" for _ in range(len(text1.split()))], db="asr")
