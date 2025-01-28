# DOWNLOADING POSTGRES INTO LOCAL PC
# MODULE: PSYCOPG2

import psycopg2
import configuration as cfg

# db_checkStatus(): Checks the connection status with the AWS RDS
#                   Returns 1 if status is READY, otherwise returns 0.
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

# db_exec(): Executes a SQL statement and commits changes to database in AWS 
def db_exec(msg):
    try:
        conn = psycopg2.connect(database=cfg.db_database, host=cfg.db_host, port=cfg.db_port, user=cfg.db_user, password=cfg.db_password)
        cursor = conn.cursor()
        cursor.execute(msg)
        conn.commit() # should commit changes to db 
        conn.close()
        return 1

    except psycopg2.Error as e:
        print(f"Error connecting to db: {e}")
        return 0

# db_createTable: Executes a CREATE TABLE command. 
#                 The arguments for this function are:
#                 (1) the name of the table >> string
#                 (2) a list of parameters >> list of (string, string list) tuples
#
#             Ex: db_createTable("test_table", [("id", ["PRIMARY KEY", "INTEGER"])])

def db_createTable(tableName,params):
    cols = ''''''
    n = len(params)
    for i in range(n):
        # param[0]: name of column
        # param[1]: list of keywords
        if i != n - 1:
            cols += f'''{params[i][0]} {" ".join(params[i][1])},'''
        else:
            cols += f'''{params[i][0]} {" ".join(params[i][1])}'''


    msg = f'''CREATE TABLE IF NOT EXISTS {tableName}({cols})'''
    db_exec(msg)

# db_dropTable: Executes a DROP TABLE command.
#               The argument for this function is the table name
#
#           Ex: db_dropTable("test_table") >> drops test_table from DB

def db_dropTable(tableName):
    msg = f'''DROP TABLE {tableName}'''
    db_exec(msg)






