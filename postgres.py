# DOWNLOADING POSTGRES INTO LOCAL PC
# MODULE: PSYCOPG2

import psycopg2
import configuration as cfg

try:
    print("Start...")
    engine = psycopg2.connect(database=cfg.db_database, host=cfg.db_host, port=cfg.db_port, user=cfg.db_user, password=cfg.db_password)
    print("Trying...")
    if engine.status == psycopg2.extensions.STATUS_READY:
        print("Connection is open and ready.")
    else:
        print("Connection is not ready")

    engine.close()

except psycopg2.Error as e:
    print("Error connecting to db: ", e)
