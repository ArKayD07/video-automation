import psycopg2

conn = psycopg2.connect(database="initial_db",
                        host="db-instance-main.c1wguimqg5ir.us-east-2.rds.amazonaws.com",
                        user="apollonian_pg",
                        password="apollonianAI2025",
                        port="5432")