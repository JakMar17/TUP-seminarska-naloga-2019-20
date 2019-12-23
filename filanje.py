import psycopg2
import mysql.connector
import time
import csv
from datetime import datetime

def csvInput(x):
    x = './csv/' + x
    return csv.reader(open(x), delimiter = ";")

seznam_pacientov = csvInput('pacient.csv')
seznam_diagnoz = csvInput('diagnoza.csv')
seznam_izvidov = csvInput('izvid.csv')
seznam_kod = csvInput('kode.csv')
seznam_obravnav = csvInput('obravnava.csv')
seznam_oddelkov = csvInput('oddelek.csv')
seznam_preiskav = csvInput('preiskava.csv')

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
                    auth_plugin='mysql_native_password'
)

postgres_cursor = postgres_connection.cursor()
mysql_cursor = mysql_connection.cursor()
print(postgres_connection)
print(mysql_connection)


def toFloat(x):
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

def postgres_pacient(cursor, database):
    stevec = 1
    header = True
    cas = 0
    query = "INSERT INTO pacient(kzz, starost, spol) VALUES (%s, %s, %s)"
    for row in seznam_pacientov:
        if header:
            header = False
            continue
        kzz = int(row[0])
        starost = int(row[1])
        spol = row[2]
        cas += insert(query, [kzz, starost, spol], cursor)
        stevec += 1
        #print(stevec)
    database.commit()
    print(cas)

def postgres_oddelek(cursor, database):
    stevec = 1
    header = True
    cas = 0
    query = "INSERT INTO oddelek(sifra_oddelka) VALUES (%s)"
    for row in seznam_oddelkov:
        if header:
            header = False
            continue
        cas += insert(query, [int(row[0])], cursor)
        stevec+=1
        #print(stevec)
    database.commit()
    print(cas)

def postgres_obravnava(cursor, database):
    stevec = 1
    header = True
    query = "INSERT INTO obravnava(st_obravnave, kzz, sifra_oddelka) VALUES (%s, %s, %s)"
    cas = 0
    for row in seznam_obravnav:
        if header:
            header = False
            continue
        kzz = int(row[0])
        obravnava = int(row[1])
        oddelek = int(row[2])
        cas += insert(query, [obravnava, kzz, oddelek], cursor)
        #print(stevec)
        stevec += 1
    database.commit()
    print(cas)

def postgres_diagnoza(cursor, database):
    stevec = 1
    header = True
    query = "INSERT INTO diagnoza(st_obravnave, st_diagnoze, ICD_diagnoze) VALUES (%s, %s, %s)"
    cas = 0
    for row in seznam_diagnoz:
        if header:
            header = False
            continue
        obravnava = int(row[0])
        diagnoza = int(row[1])
        koda = row[2]
        cas += insert(query, [obravnava, diagnoza, koda], cursor)
        #print(stevec)
        stevec += 1
    database.commit()
    print(cas)

def postgres_kode(cursor, database):
    stevec = 1
    header = True
    cas = 0
    query = "INSERT INTO MKB_koda(koda, si_naziv, en_naziv) VALUES (%s, %s, %s)"
    for row in seznam_kod:
        if header:
            header = False
            continue
        koda = row[0]
        si_naziv = row[1]
        en_naziv = row[2]
        cas += insert(query, [koda, si_naziv, en_naziv], cursor)
        #print(stevec)
        stevec += 1
    database.commit()
    print(cas)

def postgres_preiskava(cursor, database):
    stevec = 1
    header = True
    cas = 0
    query = "INSERT INTO preiskava(ime_preiskave, enota, sifra_preiskave, min_rez, max_rez, min_m, max_m, min_z, max_z) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for row in seznam_preiskav:
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
        #print(stevec)
        stevec += 1
    database.commit()
    print(cas)

def postgres_izvid(cursor, database):
    stevec = 1
    header = True
    cas = 0
    query = "INSERT INTO izvid(datum_ura, vrednost, ime_preiskave, st_obravnave) VALUES (%s, %s, %s, %s)"
    for row in seznam_izvidov:
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
    print(cas)

def timer(funkcija, cursor, database):
    casIzvajanja = 0
    t0 = time.time()
    funkcija(cursor, database)
    t1 = time.time()
    return t1-t0

#print("Pacienti")
#print(timer(postgres_pacient, postgres_cursor, postgres_connection))
#print("Oddelki")
#print(timer(postgres_oddelek, postgres_cursor, postgres_connection))
#print("Obravnave")
#print(timer(postgres_obravnava, postgres_cursor, postgres_connection))
#print("Kode")
#print(timer(postgres_kode, postgres_cursor, postgres_connection))
#print("Diagnoze")
#print(timer(postgres_diagnoza, postgres_cursor, postgres_connection))
#print("Preiskave")
#print(timer(postgres_preiskava, postgres_cursor, postgres_connection))
#print("Izvidi")
#print(timer(postgres_izvid, postgres_cursor, postgres_connection))

print("Pacienti")
print(timer(postgres_pacient, mysql_cursor, mysql_connection))
print("Oddelki")
print(timer(postgres_oddelek, mysql_cursor, mysql_connection))
print("Obravnave")
print(timer(postgres_obravnava, mysql_cursor, mysql_connection))
print("Kode")
print(timer(postgres_kode, mysql_cursor, mysql_connection))
print("Diagnoze")
print(timer(postgres_diagnoza, mysql_cursor, mysql_connection))
print("Preiskave")
print(timer(postgres_preiskava, mysql_cursor, mysql_connection))
print("Izvidi")
print(timer(postgres_izvid, mysql_cursor, mysql_connection))