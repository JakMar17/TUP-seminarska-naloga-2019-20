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

mariadb_connection = mysql.connector.connect(
                    user = "root",
                    password = "root",
                    host = "localhost",
                    port = "7203",
                    database = "[TUP]ZD",
                    auth_plugin='mysql_native_password'
)


postgres_cursor = postgres_connection.cursor()
mysql_cursor = mysql_connection.cursor()
mssql_cursor = mssql_connection.cursor()
mariadb_cursor = mariadb_connection.cursor()
print(postgres_connection)
print(mysql_connection)
print(mssql_connection)
print(mariadb_connection)

query1 = "update preiskava\
        set min_z = min_m, max_z = max_m\
        where min_z is null and max_z is null"

query2 = "update preiskava\
        set min_m = min_z, max_m = max_z\
        where min_m is null and max_m is null"


def zapisi(datoteka, vrstica):
    datoteka = open(datoteka, 'a', newline='')
    with datoteka:
        writer = csv.writer(datoteka, delimiter = ";")
        writer.writerow(vrstica)
    datoteka.close()


def testiraj(cursor, x):
    rez = []
    skupaj = 0.0
    for i in range(x):
        t = time.time()
        cursor.execute(query1)
        cursor.execute(query2)
        t1 = time.time() - t
        skupaj += t1
        rez.append(t1)
    zapisi("posodobi.csv", rez)

    return skupaj/x

def test(x):
    print("MSSQL \t" + str(testiraj(mssql_cursor, x) ))
    print("PostgreSQL \t" + str(testiraj(postgres_cursor, x) ))
    print("MariaDB: \t" + str(testiraj(mariadb_cursor, x)))
    print("MySql \t" + str(testiraj(mysql_cursor, x) ))

test(1)

t = time.time()
mysql_connection.commit()
print(time.time() - t)
t = time.time()
postgres_connection.commit()
print(time.time() - t)
t = time.time()
mssql_connection.commit()
print(time.time() - t)
t = time.time()
mariadb_connection.connect()
print(time.time() - t)