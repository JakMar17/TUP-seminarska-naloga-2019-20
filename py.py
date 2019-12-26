import psycopg2
import mysql.connector
import csv

postgres_connection = psycopg2.connect(
    user = "root",
    password = "root",
    host = "localhost",
    port = "7200",
    database = "[TUP]ZD"
)

mysql_connection = mysql.connector.connect(
    user = "root",
    password = "root",
    host = "localhost",
    port = "52000",
    database = "[TUP]ZD",
    auth_plugin = "mysql_native_password"
)

postgres_cursor = postgres_connection.cursor()
mysql_connection = mysql_connection.cursor()

def brisiIzTabele(ime_tabele, cursor, database):
    query = "DELETE FROM " + ime_tabele
    cursor.execute(query)
    database.commit()

def imenaTabel(cursor, database, tabela):
    if tabela == "MySql":
        query = "SELECT TABLE_NAME\
                FROM INFORMATION_SCHEMA.TABLES\
                WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='[TUP]ZD'"
    elif tabela == "PostgreSQL":
        query = "SELECT table_name\
                FROM information_schema.tables\
                WHERE table_schema='public'\
                AND table_type='BASE TABLE';"
    else:
        return None

    cursor.execute(query)
    rezultat = cursor.fetchall()
    print(rezultat)