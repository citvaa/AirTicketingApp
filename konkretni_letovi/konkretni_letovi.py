from datetime import datetime, timedelta, date
import time
import random
import csv
import numpy as np
from distutils import util

"""
Funkcija koja za zadati konkretni let kreira sve konkretne letove u opsegu operativnosti.
Kao rezultat vraća rečnik svih konkretnih letova koji sadrži nove konkretne letove.
"""


def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict) -> dict:
    dan = let['datum_pocetka_operativnosti']
    while dan < let['datum_kraja_operativnosti']:
        if dan.weekday() in let['dani']:
            sifra = random.randint(1000, 9999)
            datum_i_vreme_polaska = datetime.combine(dan.date(),
                                                     datetime.strptime(let['vreme_poletanja'], '%H:%M').time())
            if let['sletanje_sutra']:
                datum_i_vreme_dolaska = datetime.combine(dan.date(),
                                                         datetime.strptime(let['vreme_sletanja'], '%H:%M').time())
            else:
                datum_i_vreme_dolaska = datetime.combine(dan.date(),
                                                         datetime.strptime(let['vreme_sletanja'], '%H:%M').time())
            svi_konkretni_letovi[sifra] = {
                "sifra": sifra,
                "broj_leta": let['broj_leta'],
                "datum_i_vreme_polaska": datum_i_vreme_polaska,
                "datum_i_vreme_dolaska": datum_i_vreme_dolaska,
                # "zauzetost": podesi_matricu_zauzetosti(svi_letovi, konkretni_letovi[sifra])
            }
        dan = dan + timedelta(days=1)
    return svi_konkretni_letovi


"""
Funkcija čuva konkretne letove u fajl na zadatoj putanji sa zadatim separatorom. 
"""


def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    with open(putanja, 'w', newline='') as csvfile:
        let = ['sifra', 'broj_leta', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska', 'zauzetost']
        writer = csv.DictWriter(csvfile, fieldnames=let, delimiter=separator)
        writer.writeheader()
        for i in svi_konkretni_letovi.keys():
            writer.writerow(svi_konkretni_letovi[i])


"""
Funkcija učitava konkretne letove iz fajla na zadatoj putanji sa zadatim separatorom.
"""


def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    svi_konkretni_letovi = {}
    with open(putanja, 'r', newline='') as csvfile:
        next(csvfile)
        row = csvfile.readline().split(separator)
        zauzetost = row[4][:-2].split(';')
        for i in range(len(zauzetost)):
            zauzetost[i] = zauzetost[i].split(',')
        broj_redova = len(zauzetost)
        broj_sedista = len(zauzetost[0])
        for red in range(broj_redova):
            for sediste in range(broj_sedista):
                zauzetost[red][sediste] = util.strtobool(zauzetost[red][sediste])
                zauzetost[red][sediste] = bool(zauzetost[red][sediste])
        # print(zauzetost)
        while not row[0] == '':
            svi_konkretni_letovi[int(row[0])] = {
                'sifra': int(row[0]),
                'broj_leta': row[1],
                'datum_i_vreme_polaska': datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'),
                'datum_i_vreme_dolaska': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                'zauzetost': zauzetost
            }
            row = csvfile.readline().split(separator)
    return svi_konkretni_letovi
