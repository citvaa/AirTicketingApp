from datetime import datetime, date, timedelta
from functools import reduce

"""
Funkcija kao rezultat vraća listu karata prodatih na zadati dan.
"""


def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    lista = []
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan:
            lista.append(sve_karte[karta])
    return lista


"""
Funkcija kao rezultat vraća listu svih karata čiji je dan polaska leta na zadati dan.
"""


def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:
    lista = []
    for karta in sve_karte:
        for let in svi_konkretni_letovi:
            if sve_karte[karta]['sifra_konkretnog_leta'] == svi_konkretni_letovi[let]['sifra'] and \
                    svi_konkretni_letovi[let]['datum_i_vreme_polaska'].date() == dan:
                lista.append(sve_karte[karta])
    return lista


"""
Funkcija kao rezultat vraća listu karata koje je na zadati dan prodao zadati prodavac.
"""


def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str) -> list:
    lista = []
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan and sve_karte[karta]['prodavac'] == prodavac:
            lista.append(sve_karte[karta])
    return lista


"""
Funkcija kao rezultat vraća dve vrednosti: broj karata prodatih na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""


def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
        sve_karte: dict,
        svi_konkretni_letovi: dict,
        svi_letovi,
        dan: date
) -> tuple:
    broj = 0
    cena = 0
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan:
            broj += 1
            cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]['broj_leta']]['cena']
    tapl = (broj, cena)
    return tapl


"""
Funkcija kao rezultat vraća dve vrednosti: broj karata čiji je dan polaska leta na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""


def izvestaj_ubc_prodatih_karata_za_dan_polaska(
        sve_karte: dict,
        svi_konkretni_letovi: dict,
        svi_letovi: dict,
        dan: date
) -> tuple:
    broj = 0
    cena = 0
    for karta in sve_karte:
        for let in svi_konkretni_letovi:
            if sve_karte[karta]['sifra_konkretnog_leta'] == svi_konkretni_letovi[let]['sifra'] and \
                    svi_konkretni_letovi[let]['datum_i_vreme_polaska'] == dan:
                broj += 1
                cena += svi_letovi[svi_konkretni_letovi[let]['broj_leta']]['cena']
    tapl = (broj, cena)
    return tapl


"""
Funkcija kao rezultat vraća dve vrednosti: broj karata koje je zadati prodavac prodao na zadati dan i njihovu 
ukupnu cenu. Rezultat se vraća kao torka. Npr. return broj, suma
"""


def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(
        sve_karte: dict,
        konkretni_letovi: dict,
        svi_letovi: dict,
        dan: date,
        prodavac: str
) -> tuple:
    broj = 0
    cena = 0
    for karta in sve_karte:
        if sve_karte[karta]['datum_prodaje'] == dan and sve_karte[karta]['prodavac'] == prodavac:
            broj += 1
            cena += svi_letovi[konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]['broj_leta']]['cena']
    tapl = (broj, cena)
    return tapl


"""
Funkcija kao rezultat vraća rečnik koji za ključ ima dan prodaje, a za vrednost broj karata prodatih na taj dan.
Npr: {"2023-01-01": 20}
"""


def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(
        sve_karte: dict,
        svi_konkretni_letovi: dict,
        svi_letovi: dict
) -> dict:  # ubc znaci ukupan broj i cena
    broj = 0
    cena = 0
    izvestaj = {}
    for karta in sve_karte:
        if datetime.today().date() >= datetime.strptime(sve_karte[karta]['datum_prodaje'], '%d.%m.%Y.').date() >= (
                datetime.today().date() - timedelta(days=30)):
            broj += 1
            cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]['broj_leta']]['cena']
            if sve_karte[karta]['prodavac'] in izvestaj.keys():
                izvestaj[sve_karte[karta]['prodavac']]['broj'] += broj
                izvestaj[sve_karte[karta]['prodavac']]['cena'] += cena
            else:
                izvestaj[sve_karte[karta]['prodavac']] = {
                    'broj': broj,
                    'cena': cena
                }
    return izvestaj
