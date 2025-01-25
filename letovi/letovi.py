from datetime import datetime, timedelta, date
import re
import random
from operator import itemgetter
import csv
from distutils import util
import ast
import json

"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""


def pregled_nerealizovanih_letova(svi_letovi: dict):
    lista = []
    for let in svi_letovi:
        if svi_letovi[let]['datum_pocetka_operativnosti'] > datetime.now():
            lista.append(svi_letovi[let])
    return lista


"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""


def pretraga_letova(svi_letovi: dict, konkretni_letovi: dict, polaziste: str = "", odrediste: str = "",
                    datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "") -> list:
    lista = []

    for let in svi_letovi:
        if not svi_letovi[let][
                   'sifra_polazisnog_aerodroma'] == polaziste and not polaziste == '' and polaziste is not None:
            continue
        if not svi_letovi[let][
                   'sifra_odredisnog_aerodorma'] == odrediste and not odrediste == '' and odrediste is not None:
            continue
        if not svi_letovi[let]['vreme_poletanja'] == vreme_poletanja and not vreme_poletanja == '':
            continue
        if not svi_letovi[let]['vreme_sletanja'] == vreme_sletanja and not vreme_sletanja == '':
            continue
        if not svi_letovi[let]['prevoznik'] == prevoznik and not prevoznik == '':
            continue

        for konkretan_let in konkretni_letovi:
            if not konkretni_letovi[konkretan_let][
                       'datum_i_vreme_polaska'] == datum_polaska and datum_polaska is not None and not datum_polaska == '':
                continue
            if not konkretni_letovi[konkretan_let][
                       'datum_i_vreme_dolaska'] == datum_dolaska and datum_dolaska is not None and not datum_dolaska == '':
                continue
            if konkretni_letovi[konkretan_let]['broj_leta'] == svi_letovi[let]['broj_leta']:
                lista.append(konkretni_letovi[konkretan_let])

    return lista


"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""


def kreiranje_letova(svi_letovi: dict, broj_leta: str, sifra_polazisnog_aerodroma: str,
                     sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float, datum_pocetka_operativnosti: datetime = None,
                     datum_kraja_operativnosti: datetime = None):
    # provera validnosti podataka

    regex = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')

    if not len(broj_leta) == 4 or not broj_leta[0].isalpha() or not broj_leta[1].isalpha() or not broj_leta[
        2].isnumeric() or not broj_leta[3].isnumeric():
        raise ValueError('Broj leta mora biti oblika <slovo><slovo><cifra><cifra>')
    if not type(sifra_polazisnog_aerodroma) == str:
        raise ValueError('Sifra polazisnog aerodroma mora biti string')
    if not type(sifra_odredisnog_aerodorma) == str:
        raise ValueError("Sifra odredisnog aerodroma mora biti string")
    if not regex.match(vreme_poletanja):
        raise ValueError("Vreme poletanja mora biti oblika hh:mm")
    if not regex.match(vreme_sletanja):
        raise ValueError("Vreme sletanja mora biti oblika hh:mm")
    if not type(sletanje_sutra) == bool:
        raise ValueError("sletanje_sutra mora biti bool")
    if not type(prevoznik) == str:
        raise ValueError("Prevoznik mora biti string")
    if not type(dani) == list or len(dani) > 7 or len(dani) == 0:
        raise ValueError("Lista dani mora imati od 0-7 elemenata")
    if not type(model) == dict or not type(list(model.values())[0]) == int or not type(
            list(model.values())[1]) == str or not \
            type(list(model.values())[2]) == int or not type(list(model.values())[3]) == list:
        raise ValueError("Model mora biti dict sa ispravnim kljucevima i vrednostima")
    if not type(cena) == float:
        raise ValueError("Cena mora biti float")
    if not type(datum_pocetka_operativnosti) == datetime:
        raise ValueError("Datum pocetka operativnosti mora biti datetime")
    if not type(datum_kraja_operativnosti) == datetime:
        raise ValueError("Datum kraja operativnosti mora biti datetime")
    if datum_pocetka_operativnosti > datum_kraja_operativnosti:
        raise ValueError('Pocetak operativnosti je pre kraja operativnosti')
    else:
        svi_letovi[broj_leta] = {
            "broj_leta": broj_leta,
            "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,
            "sifra_odredisnog_aerodorma": sifra_odredisnog_aerodorma,
            "vreme_poletanja": vreme_poletanja,
            "vreme_sletanja": vreme_sletanja,
            "sletanje_sutra": sletanje_sutra,
            "prevoznik": prevoznik,
            "dani": dani,
            "model": model,
            "cena": cena,
            "datum_pocetka_operativnosti": datum_pocetka_operativnosti,
            "datum_kraja_operativnosti": datum_kraja_operativnosti
        }
        return svi_letovi


"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""


def izmena_letova(
        svi_letovi: dict,
        broj_leta: str,
        sifra_polazisnog_aerodroma: str,
        sifra_odredisnog_aerodorma: str,
        vreme_poletanja: str,
        vreme_sletanja: str,
        sletanje_sutra: bool,
        prevoznik: str,
        dani: list,
        model: dict,
        cena: float,
        datum_pocetka_operativnosti: datetime,
        datum_kraja_operativnosti: datetime
) -> dict:
    if broj_leta not in svi_letovi.keys():
        raise ValueError("Trazeni let ne postoji")

    regex = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')

    if not datum_kraja_operativnosti > datum_pocetka_operativnosti:
        raise ValueError('Pocetak operativnosti mora biti pre kraja operativnosti')
    if not len(broj_leta) == 4 or not broj_leta[0].isalpha() or not broj_leta[1].isalpha() or not broj_leta[
        2].isnumeric() or not broj_leta[3].isnumeric():
        raise ValueError('Broj leta mora biti oblika <slovo><slovo><cifra><cifra>')
    if not type(sifra_polazisnog_aerodroma) == str or not len(sifra_polazisnog_aerodroma) == 3:
        raise ValueError('Sifra polazisnog aerodroma mora biti string')
    if not type(sifra_odredisnog_aerodorma) == str or not len(sifra_odredisnog_aerodorma) == 3:
        raise ValueError("Sifra odredisnog aerodroma mora biti string")
    if not regex.match(vreme_poletanja):
        raise ValueError("Vreme poletanja mora biti oblika hh:mm")
    if not regex.match(vreme_sletanja):
        raise ValueError("Vreme sletanja mora biti oblika hh:mm")
    if not type(sletanje_sutra) == bool:
        raise ValueError("sletanje_sutra mora biti bool")
    if not type(prevoznik) == str or len(prevoznik) == 0:
        raise ValueError("Prevoznik mora biti string")
    if not type(dani) == list or len(dani) > 7 or len(dani) == 0:
        raise ValueError("Lista dani mora imati od 0-7 elemenata")
    if not type(model) == dict or not type(list(model.values())[0]) == int or not type(
            list(model.values())[1]) == str or not \
            type(list(model.values())[2]) == int or not type(list(model.values())[3]) == list:
        raise ValueError("Model mora biti dict sa ispravnim kljucevima i vrednostima")
    if not type(cena) == float:
        raise ValueError("Cena mora biti float")
    if not type(datum_pocetka_operativnosti) == datetime:
        raise ValueError("Datum pocetka operativnosti mora biti datetime")
    if not type(datum_kraja_operativnosti) == datetime:
        raise ValueError("Datum kraja operativnosti mora biti datetime")
    else:
        svi_letovi.pop(broj_leta)
        svi_letovi[broj_leta] = {
            "broj_leta": broj_leta,
            "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,
            "sifra_odredisnog_aerodorma": sifra_odredisnog_aerodorma,
            "vreme_poletanja": vreme_poletanja,
            "vreme_sletanja": vreme_sletanja,
            "sletanje_sutra": sletanje_sutra,
            "prevoznik": prevoznik,
            "dani": dani,
            "model": model,
            "cena": cena,
            "datum_pocetka_operativnosti": datum_pocetka_operativnosti,
            "datum_kraja_operativnosti": datum_kraja_operativnosti
        }
        return svi_letovi


"""
Funkcija koja cuva sve letove na zadatoj putanji
"""


def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    with open(putanja, 'w', newline='') as csvfile:
        let = ['broj_leta', "sifra_polazisnog_aerodroma", "sifra_odredisnog_aerodorma", "vreme_poletanja",
               "vreme_sletanja", "sletanje_sutra", "prevoznik", "dani", "model", "cena", "datum_pocetka_operativnosti",
               "datum_kraja_operativnosti"]
        writer = csv.DictWriter(csvfile, fieldnames=let, delimiter=separator)
        writer.writeheader()
        for i in svi_letovi.keys():
            writer.writerow(svi_letovi[i])


"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""


def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    svi_letovi = {}
    with open(putanja, 'r', newline='') as csvfile:
        next(csvfile)
        row = csvfile.readline().split(separator)
        model = ast.literal_eval(row[8])
        while not row[0] == '':
            svi_letovi[row[0]] = {
                "broj_leta": row[0],
                "sifra_polazisnog_aerodroma": row[1],
                "sifra_odredisnog_aerodorma": row[2],
                "vreme_poletanja": row[3],
                "vreme_sletanja": row[4],
                "sletanje_sutra": util.strtobool(row[5]),
                "prevoznik": row[6],
                "dani": row[7].split(),
                "model": model,
                "cena": float(row[9]),
                "datum_pocetka_operativnosti": datetime.strptime(row[10], '%Y-%m-%d %H:%M:%S'),
                "datum_kraja_operativnosti": datetime.strptime(row[11][:-2], '%Y-%m-%d %H:%M:%S')
            }
            row = csvfile.readline().split(separator)
    return svi_letovi


"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""


def podesi_matricu_zauzetosti(svi_letovi: dict, konkretni_let: dict):
    broj_leta = konkretni_let['broj_leta']
    broj_redova = svi_letovi[broj_leta]['model']['broj_redova']
    pozicije_sedista = svi_letovi[broj_leta]['model']['pozicije_sedista']
    matrica = []
    for red in range(broj_redova):
        lista_sedista = []
        for sediste in pozicije_sedista:
            lista_sedista.append(sediste)
        matrica.append(lista_sedista)
        for sediste in range(len(pozicije_sedista)):
            matrica[red][sediste] = False
    konkretni_let['zauzetost'] = matrica
    return matrica


"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""


def matrica_zauzetosti(konkretni_let: dict) -> list:
    return konkretni_let['zauzetost']


"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""


def checkin(karta, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str) -> (dict, dict):
    broj_leta = konkretni_let['broj_leta']
    if konkretni_let['datum_i_vreme_polaska'] - timedelta(hours=48) <= datetime.now():
        raise AssertionError("Checkin je prosao")
    if not 0 < red <= svi_letovi[broj_leta]['model']['broj_redova']:
        raise AssertionError('Ne postoji trazeni red')
    if pozicija not in svi_letovi[broj_leta]['model']['pozicije_sedista']:
        raise AssertionError('Ne postoji trazena pozicija')
    else:
        lista_sedista = svi_letovi[broj_leta]['model']['pozicije_sedista']
        for i in range(len(lista_sedista)):
            if lista_sedista[i] == pozicija:
                pozicija_index = i
        if konkretni_let['zauzetost'][red - 1][pozicija_index]:
            raise AssertionError('Mesto je zauzeto')
        else:
            konkretni_let['zauzetost'][red - 1][pozicija_index] = True
        karta['sediste'] = pozicija + str(red)
        return konkretni_let, karta


"""
Funkcija koja vraća listu konkretni letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""


def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    if konkretni_let['sifra'] not in svi_konkretni_letovi.keys():
        raise AssertionError('Nepostojeci let')
    broj_konkretnog_leta = konkretni_let['broj_leta']
    vreme_sletanja_konkretnog_leta = konkretni_let['datum_i_vreme_dolaska']
    lista = []
    for let in svi_konkretni_letovi:
        broj_leta = svi_konkretni_letovi[let]['broj_leta']
        if svi_letovi[broj_leta]['sifra_polazisnog_aerodroma'] == svi_letovi[broj_konkretnog_leta][
            'sifra_odredisnog_aerodorma']:
            vreme_poletanja = svi_konkretni_letovi[let]['datum_i_vreme_polaska'] - timedelta(minutes=120)
            if vreme_poletanja < vreme_sletanja_konkretnog_leta:
                lista.append(svi_konkretni_letovi[let])
    return lista


"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""


def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:
    for let in konkretni_letovi:
        if konkretni_letovi[let]['broj_leta'] not in svi_letovi.keys():
            return []
    lista = []
    for let in konkretni_letovi:
        broj_leta = konkretni_letovi[let]['broj_leta']
        polaziste_konkretnog_leta = svi_letovi[broj_leta]['sifra_polazisnog_aerodroma']
        odrediste_konkretnog_leta = svi_letovi[broj_leta]['sifra_odredisnog_aerodorma']
        if polaziste_konkretnog_leta == polaziste and odrediste_konkretnog_leta == odrediste:
            datum_polaska_konkretnog_leta = konkretni_letovi[let]['datum_i_vreme_polaska'].date()
            if datum_polaska_konkretnog_leta > (
                    datum_polaska + timedelta(days=broj_fleksibilnih_dana)) or datum_polaska_konkretnog_leta > (
                    datum_polaska - timedelta(days=broj_fleksibilnih_dana)):
                if datum_polaska_konkretnog_leta < (
                        datum_dolaska - timedelta(days=broj_fleksibilnih_dana)) or datum_polaska_konkretnog_leta < (
                        datum_dolaska + timedelta(days=broj_fleksibilnih_dana)):
                    lista.append(konkretni_letovi[let])
    return lista


def trazenje_10_najjeftinijih_letova(svi_letovi: dict, sifra_polazisnog_aerodroma: str = '',
                                     sifra_odredisnog_aerodorma: str = '') -> list:
    lista = []
    for let in svi_letovi:
        if (svi_letovi[let][
                'sifra_polazisnog_aerodroma'] == sifra_polazisnog_aerodroma or sifra_polazisnog_aerodroma == '') and (
                svi_letovi[let][
                    'sifra_odredisnog_aerodorma'] == sifra_odredisnog_aerodorma or sifra_odredisnog_aerodorma == ''):
            lista.append(svi_letovi[let])
    lista = sorted(lista, key=itemgetter('cena'))
    lista = lista[0:10]
    lista.reverse()
    return lista
