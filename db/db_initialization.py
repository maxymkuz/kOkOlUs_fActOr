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


def init_tables(connection, cursor):
    """
    Clearing up the table, and recreating them from scratch. Creating tsvector column,
    and indexing by it. Making automatic tsv from textual data on insert
    """
    # Creating asr table:
    create_table_query = """
    DROP TABLE IF EXISTS asr;
    CREATE TABLE asr
    (
        vidos_id INT NOT NULL PRIMARY KEY,
        path TEXT NOT NULL,
        title TEXT NOT NULL,
        client_id INT,
        time_added timestamp NOT NULL,
        body TEXT NOT NULL,
        tsv tsvector NOT NULL
    );
"""
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("\nTable created successfully in PostgreSQL ")

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
    print("Successfully created trigger, indexed and automized the creation of tsv!!!\n\n")

