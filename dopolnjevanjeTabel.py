import csv
import random

def nakljucna(min, max):
    return random.randint(min, max)

def nakljucnaDecimalka(min, max):
    min = float(min.replace(",", "."))
    max = float(max.replace(",", "."))
    return random.uniform(min, max)


def iskanje(niz, polje, datoteka):
    datoteka = open(datoteka)
    csv_reader = csv.reader(datoteka, delimiter = ";")
    for row in csv_reader:
        if str(niz) == str(row[polje]):
            #print(str(niz) + "  "  +  str(row[polje]))
            datoteka.close()
            return True
    datoteka.close()
    return False

def stDiagnoz(diagnoza, polje, datoteka):
    datoteka = open(datoteka)
    csv_reader = csv.reader(datoteka, delimiter = ";")
    max = 1
    for row in csv_reader:
        if str(diagnoza) == str(row[0]):
            if int(row[1]) >= max:
                max = int(row[1]) + 1
    return max

def najdiVrstico(x, datoteka):
    datoteka = open(datoteka)
    csv_reader = csv.reader(datoteka, delimiter = ";")
    stevec = 0
    for row in csv_reader:
        if stevec == x:
            x = row
            datoteka.close()
            return x
        stevec += 1
    datoteka.close()
    return None

def zapisi(datoteka, vrstica):
    #print("Vstavljam:\t" + str(vrstica))
    datoteka = open(datoteka, 'a', newline='')
    with datoteka:
        writer = csv.writer(datoteka, delimiter = ";")
        writer.writerow(vrstica)
    datoteka.close()


seznam_pacienti = 'csv/pacient.csv'
seznam_obravnav = 'csv/obravnava.csv'
seznam_oddelkov = 'csv/oddelek.csv'
seznam_preiskav = 'csv/preiskava.csv'
seznam_izvidov = 'csv/izvid.csv'
seznam_kod = 'csv/kode.csv'
seznam_diagnoz = 'csv/diagnoza.csv'

def filanjeObravnav(stevec):
    obravnava = 26326
    i = 0
    while i < stevec:
        obravnava += 1
        kzz = nakljucna(500001, 508219)
        oddelek = nakljucna(2300, 2309)
        #print("naključna: " + str(kzz))
        if iskanje(kzz, 0, seznam_pacienti):
            if iskanje(oddelek, 0, seznam_oddelkov):
                zapisi(seznam_obravnav, [kzz, obravnava, oddelek])
                print(i)
                i += 1

def filanjeIzvidov(stevec):
    i = 0
    while i < stevec:
        obravnava = nakljucna(30000, 53502)
        if iskanje(obravnava, 1,seznam_obravnav):
            preiskava = nakljucna(2, 274)
            preiskava = najdiVrstico(preiskava, seznam_preiskav)
            datum_ura = "22.12.2019 22:52"
            parameter = preiskava[0]
            vrednost = nakljucnaDecimalka(preiskava[2], preiskava[3])
            zapisi(seznam_izvidov, [obravnava, datum_ura, parameter, vrednost])
            print(i)
            i+=1
filanjeIzvidov(10000)


def filanjeDiagnoz(stevec):
    i = 0
    while i < stevec:
        obravnava = nakljucna(30000, 53502)
        if iskanje(obravnava, 1, seznam_obravnav):
            stDiagnoze = stDiagnoz(obravnava, 0, seznam_diagnoz)
            diagnoza = nakljucna(2, 18955)
            diagnoza = najdiVrstico(diagnoza, seznam_kod)
            if diagnoza == None:
                continue
            diagnoza = diagnoza[0]
            zapisi(seznam_diagnoz, [obravnava, stDiagnoze, diagnoza])
            print(i)
            i+=1

#filanjeDiagnoz(30000)
