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


def toFloat(x):
    x = x.replace(",", ".")
    try:
        y = float(x)
    except ValueError:
        y = None
    return y

def toDate(x):
    date = datetime.strptime(x, "%d.%m.%Y %H:%M")
    date.strftime("%Y-%m-%d %H:%M:%S")
    return date

def insert(query, input, cursor):
    tt0 = time.time()
    cursor.execute(query, input)
    return time.time() - tt0

def povprecje(table):
    if not table:
        return 0
    header = True
    x = 0.0
    stevec = 0
    for i in table:
        if header or i is None:
            header = False
            continue
        x += i
        stevec +=1
    if stevec is 0:
        return 0
    return x/stevec

def timer(funkcija, cursor, database):
    return funkcija(cursor, database)

def zapisi(datoteka, vrstica):
    #print("Vstavljam:\t" + str(vrstica))
    datoteka = open(datoteka, 'a', newline='')
    with datoteka:
        writer = csv.writer(datoteka, delimiter = ";")
        writer.writerow(vrstica)
    datoteka.close()


## Metode za polnjenje MySQL in PostgreSQL podatkovnih baz ##

def pacient(cursor, database):
    header = True
    cas = 0
    query = "INSERT INTO pacient(kzz, starost, spol) VALUES (%s, %s, %s)"
    for row in csvInput('pacient.csv'):
        if header:
            header = False
            continue
        kzz = int(row[0])
        starost = int(row[1])
        spol = row[2]
        cas += insert(query, ([kzz, starost, spol]), cursor)
    database.commit()
    return cas

def oddelek(cursor, database):
    header = True
    cas = 0
    query = "INSERT INTO oddelek(sifra_oddelka) VALUES (%s)"
    for row in csvInput('oddelek.csv'):
        if header:
            header = False
            continue
        cas += insert(query, [int(row[0])], cursor)
    database.commit()
    return cas

def obravnava(cursor, database):
    header = True
    query = "INSERT INTO obravnava(st_obravnave, kzz, sifra_oddelka) VALUES (%s, %s, %s)"
    cas = 0
    for row in csvInput('obravnava.csv'):
        if header:
            header = False
            continue
        kzz = int(row[0])
        obravnava = int(row[1])
        oddelek = int(row[2])
        cas += insert(query, [obravnava, kzz, oddelek], cursor)
    database.commit()
    return cas

def diagnoza(cursor, database):
    header = True
    query = "INSERT INTO diagnoza(st_obravnave, st_diagnoze, ICD_diagnoze) VALUES (%s, %s, %s)"
    cas = 0
    for row in csvInput('diagnoza.csv'):
        if header:
            header = False
            continue
        obravnava = int(row[0])
        diagnoza = int(row[1])
        koda = row[2]
        cas += insert(query, [obravnava, diagnoza, koda], cursor)
    database.commit()
    return cas

def kode(cursor, database):
    header = True
    cas = 0
    query = "INSERT INTO MKB_koda(koda, si_naziv, en_naziv) VALUES (%s, %s, %s)"
    for row in csvInput('kode.csv'):
        if header:
            header = False
            continue
        koda = row[0]
        si_naziv = row[1]
        en_naziv = row[2]
        cas += insert(query, [koda, si_naziv, en_naziv], cursor)
    database.commit()
    return cas

def preiskava(cursor, database):
    header = True
    cas = 0
    query = "INSERT INTO preiskava(ime_preiskave, enota, sifra_preiskave, min_rez, max_rez, min_m, max_m, min_z, max_z) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for row in csvInput('preiskava.csv'):
        if header:
            header = False
            continue
        naziv = row[0]
        sifra = int(row[1])
        minSI = toFloat(row[2])
        maxSI = toFloat(row[3])
        minM = toFloat(row[4])
        maxM = toFloat(row[5])
        minZ = toFloat(row[6])
        maxZ = toFloat(row[7])
        enota = row[8]
        cas += insert(query, [naziv, enota, sifra, minSI, maxSI, minM, maxM, minZ, maxZ], cursor)
    database.commit()
    return cas

def izvid(cursor, database):
    stevec = 1
    header = True
    cas = 0
    query = "INSERT INTO izvid(datum_ura, vrednost, ime_preiskave, st_obravnave) VALUES (%s, %s, %s, %s)"
    for row in csvInput('izvid.csv'):
        if header:
            header = False
            continue
        obravnava = int(row[0])
        datum_ura = toDate(row[1])
        preiskava = row[2]
        vrednost = toFloat(row[3])
        cas += insert(query, [datum_ura, vrednost, preiskava, obravnava], cursor)
        #print(stevec)
        stevec += 1
    database.commit()
    return cas



## Metode za polnjenje MsSQL Server podatkovne baze ##

def mssql_pacient(cursor, database):
    header = True
    cas = 0
    query = "INSERT INTO pacient(kzz, starost, spol) VALUES (?, ?, ?)"
    for row in csvInput('pacient.csv'):
        if header:
            header = False
            continue
        kzz = int(row[0])
        starost = int(row[1])
        spol = row[2]
        cas += insert(query, [kzz, starost, spol], cursor)
    database.commit()
    return cas

def mssql_oddelek(cursor, database):
    header = True
    cas = 0
    query = "INSERT INTO oddelek(sifra_oddelka) VALUES (?)"
    for row in csvInput('oddelek.csv'):
        if header:
            header = False
            continue
        cas += insert(query, [int(row[0])], cursor)
    database.commit()
    return cas

def mssql_obravnava(cursor, database):
    header = True
    query = "INSERT INTO obravnava(st_obravnave, kzz, sifra_oddelka) VALUES (?, ?, ?)"
    cas = 0
    for row in csvInput('obravnava.csv'):
        if header:
            header = False
            continue
        kzz = int(row[0])
        obravnava = int(row[1])
        oddelek = int(row[2])
        cas += insert(query, [obravnava, kzz, oddelek], cursor)
    database.commit()
    return cas

def mssql_diagnoza(cursor, database):
    header = True
    query = "INSERT INTO diagnoza(st_obravnave, st_diagnoze, ICD_diagnoze) VALUES (?, ?, ?)"
    cas = 0
    for row in csvInput('diagnoza.csv'):
        if header:
            header = False
            continue
        obravnava = int(row[0])
        diagnoza = int(row[1])
        koda = row[2]
        cas += insert(query, [obravnava, diagnoza, koda], cursor)
    database.commit()
    return cas

def mssql_kode(cursor, database):
    header = True
    cas = 0
    query = "INSERT INTO MKB_koda(koda, si_naziv, en_naziv) VALUES (?, ?, ?)"
    for row in csvInput('kode.csv'):
        if header:
            header = False
            continue
        koda = row[0]
        si_naziv = row[1]
        en_naziv = row[2]
        cas += insert(query, [koda, si_naziv, en_naziv], cursor)
    database.commit()
    return cas

def mssql_preiskava(cursor, database):
    header = True
    cas = 0
    query = "INSERT INTO preiskava(ime_preiskave, enota, sifra_preiskave, min_rez, max_rez, min_m, max_m, min_z, max_z) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    for row in csvInput('preiskava.csv'):
        if header:
            header = False
            continue
        naziv = row[0]
        sifra = int(row[1])
        minSI = toFloat(row[2])
        maxSI = toFloat(row[3])
        minM = toFloat(row[4])
        maxM = toFloat(row[5])
        minZ = toFloat(row[6])
        maxZ = toFloat(row[7])
        enota = row[8]
        cas += insert(query, [naziv, enota, sifra, minSI, maxSI, minM, maxM, minZ, maxZ], cursor)
    database.commit()
    return cas

def mssql_izvid(cursor, database):
    stevec = 1
    header = True
    cas = 0
    query = "INSERT INTO izvid(datum_ura, vrednost, ime_preiskave, st_obravnave) VALUES (?, ?, ?, ?)"
    for row in csvInput('izvid.csv'):
        if header:
            header = False
            continue
        obravnava = int(row[0])
        datum_ura = toDate(row[1])
        preiskava = row[2]
        vrednost = toFloat(row[3])
        cas += insert(query, [datum_ura, vrednost, preiskava, obravnava], cursor)
        #print(stevec)
        stevec += 1
    database.commit()
    return cas



def deleteFrom(table, cursor, database):
    query = "DELETE FROM " + table
    cursor.execute(query)
    database.commit()

def napolniBazo_MySql():
    skupenCas = 0

    print("MySQL")

    t = timer(pacient, mysql_cursor, mysql_connection)
    print("Pacient:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(oddelek, mysql_cursor, mysql_connection)
    print("Oddelek:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(obravnava, mysql_cursor, mysql_connection)
    print("Obravnava:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(kode, mysql_cursor, mysql_connection)
    print("Kode:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(diagnoza, mysql_cursor, mysql_connection)
    print("Diagnoza:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(preiskava, mysql_cursor, mysql_connection)
    print("Preiskava:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(izvid, mysql_cursor, mysql_connection)
    print("Izvid:\t" + str("%.5f" %t))
    skupenCas += t

    print("%.5f" % skupenCas)
    return skupenCas
    
def napolniBazo_Postgres():
    skupenCas = 0   

    print("PostgreSQL")

    t = timer(pacient, postgres_cursor, postgres_connection)
    print("Pacient:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(oddelek, postgres_cursor, postgres_connection)
    print("Oddelek:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(obravnava, postgres_cursor, postgres_connection)
    print("Obravnava:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(kode, postgres_cursor, postgres_connection)
    print("Kode:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(diagnoza, postgres_cursor, postgres_connection)
    print("Diagnoza:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(preiskava, postgres_cursor, postgres_connection)
    print("Preiskava:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(izvid, postgres_cursor, postgres_connection)
    print("Izvid:\t" + str("%.5f" %t))
    skupenCas += t

    print("%.5f" % skupenCas)
    return skupenCas

def napolniBazo_MsSQL():
    skupenCas = 0   

    print("Microsoft SQL Server")

    t = timer(mssql_pacient, mssql_cursor, mssql_connection)
    print("Pacient:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(mssql_oddelek, mssql_cursor, mssql_connection)
    print("Oddelek:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(mssql_obravnava, mssql_cursor, mssql_connection)
    print("Obravnava:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(mssql_kode, mssql_cursor, mssql_connection)
    print("Kode:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(mssql_diagnoza, mssql_cursor, mssql_connection)
    print("Diagnoza:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(mssql_preiskava, mssql_cursor, mssql_connection)
    print("Preiskava:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(mssql_izvid, mssql_cursor, mssql_connection)
    print("Izvid:\t" + str("%.5f" %t))
    skupenCas += t

    print("%.5f" % skupenCas)
    return skupenCas

    
def izprazniBazo(cursor, database, imenaTabel):
    t0 = time.time()
    for tabela in imenaTabel:
        deleteFrom(tabela[0], cursor, database)
    t1 = time.time() - t0
    print(t1)

def dobiImenaTabel(cursor, query):
    cursor.execute(query)
    rezultat = cursor.fetchall()
    return rezultat


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

#izprazniBazo(mssql_cursor, mssql_connection, dobiImenaTabel(mssql_cursor, mssql_query))
#izprazniBazo(mysql_cursor, mysql_connection, dobiImenaTabel(mysql_cursor, mysql_query))
#izprazniBazo(postgres_cursor, postgres_connection, dobiImenaTabel(postgres_cursor, postgres_query))

t_mysql = ["MySQL vstavljanje"]
t_postgres = ["PostgreSQL vstavljanje"]
t_mssql = ["MS SQL Server vstavljanje"]

td_mysql = ["MySQL brisanje"]
td_postgres = ["PostgreSQL brisanje"]
td_mssql = ["MS SQL brisanje"]


def testiraj(x):
    for i in range(x):
        print("tukaj")
        td_mssql.append(izprazniBazo(mssql_cursor, mssql_connection, dobiImenaTabel(mssql_cursor, mssql_query)))
        td_mysql.append(izprazniBazo(mysql_cursor, mysql_connection, dobiImenaTabel(mysql_cursor, mysql_query)))
        td_postgres.append(izprazniBazo(postgres_cursor, postgres_connection, dobiImenaTabel(postgres_cursor, postgres_query)))
        td_postgres.append(izprazniBazo(mariadb_cursor, mariadb_connection, dobiImenaTabel(mariadb_cursor, mysql_query)))

        print("\n\n" + str(i+1))

        napolniBazo_mariadb()

        print("\n")

        napolniBazo_MsSQL()
        #t_mssql.append(napolniBazo_MsSQL())

        print("\n")

        napolniBazo_MySql()
        #t_mysql.append(napolniBazo_MySql())

        print("\n")

        napolniBazo_Postgres()
        #t_postgres.append(napolniBazo_Postgres())

        print("\n")


    print(".....................")
    print("Vstavljanje MySql: " + str(t_mysql))
    print(povprecje(t_mysql))
    print("Vstavljanje PostgreSQL: " + str(t_postgres))
    print(povprecje(t_postgres))
    print("Vstavljanje Microsoft SQL Server: " + str(t_mssql))
    print(povprecje(t_mssql))
    print()
    print("Brisanje MySql: " + str(td_mysql))
    print(povprecje(td_mysql))
    print("Brisanje PostgreSQL: " + str(td_postgres))
    print(povprecje(td_postgres))
    print("Brisanje Microsoft SQL Server: " + str(td_mssql))
    print(povprecje(td_mssql))

    v_rez = "vstavi.csv"
    d_rez = "brisi.csv"
    zapisi(v_rez, t_mysql)
    zapisi(d_rez, td_mysql)
    zapisi(v_rez, t_postgres)
    zapisi(d_rez, td_postgres)
    zapisi(v_rez, t_mssql)
    zapisi(d_rez, td_postgres)

def napolniBazo_mariadb():
    skupenCas = 0

    print("MariaDB")

    t = timer(pacient, mariadb_cursor, mariadb_connection)
    print("Pacient:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(oddelek, mariadb_cursor, mariadb_connection)
    print("Oddelek:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(obravnava, mariadb_cursor, mariadb_connection)
    print("Obravnava:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(kode, mariadb_cursor, mariadb_connection)
    print("Kode:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(diagnoza, mariadb_cursor, mariadb_connection)
    print("Diagnoza:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(preiskava, mariadb_cursor, mariadb_connection)
    print("Preiskava:\t" + str("%.5f" %t))
    skupenCas += t

    t = timer(izvid, mariadb_cursor, mariadb_connection)
    print("Izvid:\t" + str("%.5f" %t))
    skupenCas += t

    print("%.5f" % skupenCas)
    return skupenCas

testiraj(1)

#izprazniBazo(mariadb_cursor, mariadb_connection, dobiImenaTabel(mariadb_cursor, mysql_query))
#napolniBazo_mariadb()
