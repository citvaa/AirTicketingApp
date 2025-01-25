import random
import csv


"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""


def kreiranje_modela_aviona(
        svi_modeli_aviona: dict,
        naziv: str = "",
        broj_redova: str = "",
        pozicije_sedista: list = []
) -> dict:
    if naziv == '' or broj_redova == '' or pozicije_sedista == '':
        raise ValueError('Nevalidni argumenti')
    if naziv is None or broj_redova is None or pozicije_sedista is None:
        raise ValueError('Nevalidni argumenti')
    else:
        id = random.randint(1000, 9999)
        svi_modeli_aviona[id] = {
            'id': id,
            'naziv': naziv,
            'broj_redova': broj_redova,
            'pozicije_sedista': pozicije_sedista
        }
        return svi_modeli_aviona


"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""


def sacuvaj_modele_aviona(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, 'w', newline='') as csvfile:
        avion = ['id', 'naziv', 'broj_redova', 'pozicije_sedista']
        writer = csv.DictWriter(csvfile, fieldnames=avion, delimiter=separator)
        writer.writeheader()
        for i in svi_aerodromi.keys():
            writer.writerow(svi_aerodromi[i])


"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""


def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    svi_modeli_aviona = {}
    with open(putanja, 'r', newline='') as csvfile:
        next(csvfile)
        row = csvfile.readline().split(separator)
        while not row[0] == '':
            svi_modeli_aviona[row[0]] = {
                'id': row[0],
                'naziv': row[1],
                'broj_redova': row[2],
                'pozicije_sedista': row[3].split()
            }
            row = csvfile.readline().split(separator)
    return svi_modeli_aviona
