import psycopg2
import mysql.connector
import pyodbc
import time
import csv
from datetime import datetime

def csvInput(x):
    x = './csv/' + x
    return csv.reader(open(x), delimiter = ";")

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
                    port = "7202",
                    database = "[TUP]ZD",
                    auth_plugin='mysql_native_password'
)

mssql_connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};\
    SERVER=tcp:localhost,7201;\
    DATABASE=[TUP]ZD;\
    UID=sa;\
    PWD=root_ROOT'
)

postgres_cursor = postgres_connection.cursor()
mysql_cursor = mysql_connection.cursor()
mssql_cursor = mssql_connection.cursor()
print(postgres_connection)
print(mysql_connection)
print(mssql_connection)


mysql_query = "SELECT TABLE_NAME\
                FROM INFORMATION_SCHEMA.TABLES\
                WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='[TUP]ZD'"
postgres_query = "SELECT table_name\
                FROM information_schema.tables\
                WHERE table_schema='public'\
                AND table_type='BASE TABLE';"
mssql_query = "SELECT TABLE_NAME\
                FROM INFORMATION_SCHEMA.TABLES\
                WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='dbo'"


def dobiImenaTabel(cursor, query):
    cursor.execute(query)
    rezultat = cursor.fetchall()
    return rezultat

def prestejVrstice(cursor, tabele):
    skupaj = 0
    for tabela in tabele:
        query = "SELECT COUNT(*) FROM " + tabela[0]
        cursor.execute(query)
        y = cursor.fetchone()
        skupaj += y[0]
    return skupaj

print("Število vrstic MySql: " + str(prestejVrstice(mysql_cursor, dobiImenaTabel(mysql_cursor, mysql_query))))
print("Število vrstic PostgreSQL: " + str(prestejVrstice(postgres_cursor, dobiImenaTabel(postgres_cursor, postgres_query))))
print("Število vrstic MSSQL: " + str(prestejVrstice(mssql_cursor, dobiImenaTabel(mssql_cursor, mssql_query))))