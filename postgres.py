# DOWNLOADING POSTGRES INTO LOCAL PC
# MODULE: PSYCOPG2

import psycopg2
import configuration as cfg


def db_checkStatus():
    try:
        conn = psycopg2.connect(database=cfg.db_database, host=cfg.db_host, port=cfg.db_port, user=cfg.db_user, password=cfg.db_password)
        db_status = 0
        if conn.status == psycopg2.extensions.STATUS_READY:
            db_status = 1
        else:
            db_status = 0
        
        conn.close()
        return db_status
    
    except psycopg2.Error as e:
        print(f"Error connecting to db: {e}")


def db_exec(msg):
    try:
        conn = psycopg2.connect(database=cfg.db_database, host=cfg.db_host, port=cfg.db_port, user=cfg.db_user, password=cfg.db_password)
        cursor = conn.cursor()
        cursor.execute(msg)
        conn.commit() # should commit changes to db 
        conn.close()

    except psycopg2.Error as e:
        print(f"Error connecting to db: {e}")

table_name = "tabletest"
test_msg = f''' 
            CREATE TABLE IF NOT EXISTS {table_name}(
                id INTEGER PRIMARY KEY NOT NULL,
                text_field TEXT 
            )
            '''


