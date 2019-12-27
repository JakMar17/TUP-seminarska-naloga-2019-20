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

query1_join = "select p.kzz, p.spol, o.st_obravnave, i.ime_preiskave, i.vrednost\
                from pacient p\
                inner join obravnava o on o.kzz = p.kzz\
                inner join izvid i on i.st_obravnave = o.st_obravnave\
                order by p.kzz, o.st_obravnave"

query1_where = "select p.kzz, p.spol, o.st_obravnave, i.ime_preiskave, i.vrednost\
                from pacient p, obravnava o, izvid i\
                where p.kzz = o.kzz and o.st_obravnave = i.st_obravnave\
                order by p.kzz, o.st_obravnave"

query2 = "select i.ime_preiskave, count(i.ime_preiskave)\
            from izvid i\
            inner join obravnava o on i.st_obravnave = o.st_obravnave\
            inner join pacient p on p.kzz = o.kzz\
            inner join preiskava p2 on i.ime_preiskave = p2.ime_preiskave\
            where\
                (p.spol = 'M' and p2.max_m <= i.vrednost and p2.max_m is not null) or\
                (p.spol = 'Z' and p2.max_z <= i.vrednost and p2.max_z is not null)\
            group by i.ime_preiskave\
            order by count(i.ime_preiskave) desc"

query3 = "select ime_preiskave, count(vrednost), min(vrednost), max(vrednost), avg(vrednost)\
            from izvid\
            group by ime_preiskave\
            having count(vrednost) > 200 and avg(vrednost) * 2 <= max(vrednost)\
            order by count(vrednost) desc, ime_preiskave asc"

query4 = "select m.si_naziv, count(o.st_obravnave) as Stevilo,\
            (\
                select min(p1.starost)\
                    from\
                        pacient p1,\
                        obravnava o1,\
                        diagnoza d1,\
                        MKB_koda m1\
                    where\
                        p1.kzz = o1.kzz and\
                        d1.st_obravnave = o1.st_obravnave and\
                        d1.icd_diagnoze = m1.koda and\
                        m1.si_naziv = m.si_naziv\
            ) as min,\
            (\
                select max(p1.starost)\
                    from\
                        pacient p1,\
                        obravnava o1,\
                        diagnoza d1,\
                        MKB_koda m1\
                    where\
                        p1.kzz = o1.kzz and\
                        d1.st_obravnave = o1.st_obravnave and\
                        d1.icd_diagnoze = m1.koda and\
                        m1.si_naziv = m.si_naziv\
            ) as max,\
            (\
                select avg(p1.starost)\
                    from\
                        pacient p1,\
                        obravnava o1,\
                        diagnoza d1,\
                        MKB_koda m1\
                    where\
                        p1.kzz = o1.kzz and\
                        d1.st_obravnave = o1.st_obravnave and\
                        d1.icd_diagnoze = m1.koda and\
                        m1.si_naziv = m.si_naziv\
            ) as povprecje\
        from pacient p\
            inner join obravnava o on p.kzz = o.kzz\
            inner join diagnoza d on o.st_obravnave = d.st_obravnave\
            inner join MKB_koda m on m.koda = d.icd_diagnoze\
            inner join izvid i on d.st_obravnave = i.st_obravnave\
            inner join preiskava p2 on i.ime_preiskave = p2.ime_preiskave\
            where\
                p.starost between 21 and 40 and\
                m.si_naziv like '%trčen%'\
            group by m.si_naziv, p.starost\
            order by count(o.st_obravnave) desc"


def zapisi(datoteka, vrstica):
    datoteka = open(datoteka, 'a', newline='')
    with datoteka:
        writer = csv.writer(datoteka, delimiter = ";")
        writer.writerow(vrstica)
    datoteka.close()


def testirajPoizvedbo(cursor, query, x):
    rez = []
    skupaj = 0.0
    for i in range(x):
        t = time.time()
        cursor.execute(query);
        t1 = time.time() - t
        skupaj += t1
        rez.append(t1)
        cursor.fetchall()
    zapisi("poizvedba.csv", rez)

    return skupaj/x

def test(x, query):
    print("MSSQL \t" + str(testirajPoizvedbo(mssql_cursor, query, x) ))
    print("PostgreSQL \t" + str(testirajPoizvedbo(postgres_cursor, query, x) ))
    print("MySql \t" + str(testirajPoizvedbo(mysql_cursor, query, x) ))

#test(10, query1_join)
#print()
#test(10, query1_where)
#print()
#test(10, query2)

#test(100, query3)
test(1, query4)