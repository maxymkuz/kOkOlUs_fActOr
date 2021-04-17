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


def init_table_asr(connection, cursor):
    """
    Clearing up the ASR table, and recreating them from scratch. Creating tsvector column,
    and indexing by it. Making automatic tsv from textual data on insert
    """
    # Creating asr table:
    create_table_query = """
    DROP TABLE IF EXISTS asr;
    CREATE TABLE asr
    (
        video_id TEXT NOT NULL,
        title TEXT NOT NULL,
        client_id INT,
        time_added timestamp NOT NULL,
        body TEXT NOT NULL,
        timestamps TEXT[] NOT NULL,
        text_as_array TEXT[] NOT NULL,
        tsv tsvector NOT NULL
    );
"""
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("\nTable ASR created successfully in PostgreSQL ")

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
    print("Successfully created ASR trigger, indexed and automized the creation of tsv!!!\n\n")


def init_table_ocr(connection, cursor):
    """
    Clearing up the OCR table, and recreating them from scratch. Creating tsvector column,
    and indexing by it. Making automatic tsv from textual data on insert
    """
    # Creating ocr table:
    create_table_query = """
    DROP TABLE IF EXISTS ocr;
    CREATE TABLE ocr
    (
        video_id TEXT NOT NULL,
        title TEXT NOT NULL,
        client_id INT,
        time_added timestamp NOT NULL,
        body TEXT NOT NULL,
        timestamps TEXT[] NOT NULL,
        text_as_array TEXT[] NOT NULL,
        tsv tsvector NOT NULL
    );
"""
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("\nTable OCR created successfully in PostgreSQL ")

    create_update_tsv(connection, cursor)
    create_index = """
    CREATE INDEX ocr_index
        ON ocr USING gin (tsv);
    """
    create_tsv_trigger = """
    CREATE TRIGGER update_tsv
       BEFORE INSERT OR UPDATE ON ocr
       FOR EACH ROW EXECUTE PROCEDURE update_tsv();
    """
    cursor.execute(create_index)
    cursor.execute(create_tsv_trigger)
    connection.commit()
    print("Successfully created OCR trigger, indexed and automized the creation of tsv!!!\n\n")



