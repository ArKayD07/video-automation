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
        cols += f'''{params[i][0]} {" ".join(params[i][1])},''' if (i != n - 1) else f'''{params[i][0]} {" ".join(params[i][1])}'''

    msg = f'''CREATE TABLE IF NOT EXISTS {tableName}({cols})'''
    db_exec(msg)

# db_dropTable: Executes a DROP TABLE command.
#               The argument for this function is the table name
#
#           Ex: db_dropTable("test_table") >> drops test_table from DB

def db_dropTable(tableName):
    msg = f'''DROP TABLE {tableName}'''
    db_exec(msg)

# db_insert: Executes an INSERT INTO command (inserts a new record).
#            The arguments for this function are:
#            (1) the name of the table >> string
#            (2) a list of parameters >> list of (string, string) tuples
#
#             Ex: db_insert("test_table", [("name","\"Sebastian\""),("code", "0101")])

def db_insert(tableName,params):
    cols = ''''''
    vals = ''''''
    n = len(params)
    for i in range(n):
        # param[i][0]: name of column
        # param[i][1]: value inserted
        cols += f'''{params[i][0]},''' if (i != n - 1) else f'''{params[i][0]}'''
        vals += f'''{params[i][1]},''' if (i != n - 1) else f'''{params[i][1]}'''

    msg = f'''INSERT INTO {tableName} ({cols}) VALUES ({vals})'''
    db_exec(msg)

# db_query: Executes a SELECT statement (queries from a table).
#           The arguments for this function are:
#           (1) the name of the table >> string
#           (2) a list of columns for the query >> string list
#           (3) a string with a conditional WHERE statement >> string
#
#       Ex: db_query("test_table",["name","code"],"name=\"Sebastian\" AND code=0101")

def db_query(tableName,cols,conds):
    selectCols = ",".join(cols) if (len(cols) != 0) else "*"
    conditions = f'''WHERE {conds}''' if (len(conds) != 0) else ''''''
    msg = f'''SELECT {selectCols} FROM {tableName} {conditions}'''
    db_exec(msg)

# db_delete: Executes a DELETE statement (deletes a record).
#            The arguments for this function are:
#            (1) the name of the table >> string
#            (2) a string with a conditional WHERE statement >> string
#
#        Ex: db_delete("test_table","name=\"Sebastian\"")

def db_delete(tableName,conds):
    msg = f'''DELETE FROM {tableName} WHERE {conds}'''
    db_exec(msg)