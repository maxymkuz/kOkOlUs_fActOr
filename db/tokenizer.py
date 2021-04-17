def tokenize_word(connection, cursor, word):
    sql_querry = """
    SELECT * FROM to_tsvector('english', %s);
    """
    cursor.execute(sql_querry, [word])
    res = cursor.fetchall()[0]
    return res[0].split(":")[0].replace("'", "")
