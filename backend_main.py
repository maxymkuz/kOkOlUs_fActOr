from db.connection import connect_to_db, disconnect
from db.db_manipulator import search_db, insert_db
from db.db_initialization import init_table_asr, init_table_ocr


def find_db(connection, cursor, query, db="asr"):
    """
    Query: has to be of
    """
    query_for_db = "&".join(query.split())
    db_ans = search_db(connection, cursor, query_for_db, db=db)
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

    text3 = "images are actually physically formed we need to understand biology and psychology to understand how a how animal brains out physically see and process visual information we of course draw a lot on computer science mathematics and engineering as we actually strive to build computer systems that implements are our computer vision algorithms so a little bit more about about where i'm coming from and about where the teaching staff of this course is coming from me and my co instructor serena are both phd students in the stanford vision lab who it which is headed by professor fei fei li and our lab really focuses on machine learning and computer science side of things i work a little bit more on language and vision i've done some projects than that and other folks in our group have worked a little bit on the neuroscience and cognitive science side of things so as a bit of introduction you might be curious about how this course relates to other courses at stanford so we kind of assume a basic introductory level understanding of computer vision so if you're kind of an undergrad and you've never seen computer vision before maybe you should have taken cs one thirty one which was offered earlier this year by faye faye and juan carlos new place there was a course lack taught last quarter by by professor chris manning and richard soldier about the intersection of deep learning and natural language processing and i imagine the number of you may have taken that course last quarter but we're we will cover some of the will they'll be some overlap between this course and that but we're really focusing on the computer vision asp side of things and really focusing all of our motivation in computer vision also concurrently taught this quarter is cs two three one a taught by professor silvio summer aussie and this and see us to if they want a really focuses on is a more all encompassing computer vision course it's focusing on things like three db construction come on matching and robotic vision and is a bit more all encompassing with her guards division than our course and this course cs truth you want and really focuses on a particular class of algorithms revolving around neural networks and especially convolution on their own networks and their applications to various visual recognition tasks of course there's also a number of seminar courses that are taught and you'll have to check the syllabus and course schedule for more details on those because they vary a bit each year so this lecture is normally given by by professor fei fei li unfortunately she wasn't able to be here today so instead for the majority of electorate we're going to tag team a little bit so she actually recorded a bit of pre recorded audio describing to the history of computer vision because this class is a computer vision course and it's very critical and important that you understand the history and the context of all the existing work that led us to these developments of convolution neural networks as we know them today i'll let virtual faye faye take over and and give you a brief introduction to the history of computer vision okay let's start with that today's agenda so we have two topics to cover one is a brief history of computer vision and other one is the overview of course cs two thirty one and so we'll start with a very brief history of where vision comes come from when did computer vision stipe and where we are today the history the history of vision can go back many many years ago in fact about five hundred forty three million years ago what was life like during that time well the earth was mostly water there were a few few species of animals floating around in the ocean and life was very chill animals did a move around much that they don't have eyes or anything when food swims by they grab them if the food didn't swim by they just float around but something really remarkable happened around five hundred forty million years ago from fossil studies zoologists found out within a very short period of time ten million years the number of animal species just"
    insert_db(connection, cursor, 0, "_", "second title one",
              text1.split(), ["RAndom_timestamp" for _ in range(len(text1.split()))], db="asr")
    insert_db(connection, cursor, 1, "_", "first title one",
              text2.split(), ["RAndom_timestamp" for _ in range(len(text2.split()))], db="asr")
    insert_db(connection, cursor, 2, "_", "volodya cv",
              text3.split(), ["r_t" for _ in range(len(text3.split()))], db="asr")

    print()

    search_result = find_db(connection, cursor, "Computers vision", db="asr")
    print(search_result)


if __name__ == '__main__':
    main()
