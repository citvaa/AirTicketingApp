from common import konstante
from functools import reduce
from datetime import datetime
import csv
import json

"""
Brojačka promenljiva koja se automatski povećava pri kreiranju nove karte.
"""
sledeci_broj_karte = 1

"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""


def kupovina_karte(
        sve_karte: dict,
        svi_konkretni_letovi: dict,
        sifra_konkretnog_leta: int,
        putnici: list,
        slobodna_mesta: list,
        kupac: dict,
        **kwargs
) -> (dict, dict):
    if sifra_konkretnog_leta not in svi_konkretni_letovi.keys():
        raise ValueError('Ne postoji konkretan let')
    brojac = 0
    for red in range(len(slobodna_mesta)):
        for sediste in range(len(slobodna_mesta[red])):
            if not slobodna_mesta[red][sediste]:
                brojac += 1
    if brojac == 0:
        raise ValueError('Nema slobodnih mesta')
    if not type(sifra_konkretnog_leta) == int:
        raise ValueError('Sifra mora biti int')
    if not type(putnici) == list:
        raise ValueError('Putnici moraju biti list')
    if not type(slobodna_mesta) == list:
        raise ValueError('Slobodna mesta moraju biti list')
    if not type(kupac) == dict:
        raise ValueError('Kupac mora biti dict')
    else:
        sve_karte[sledeci_broj_karte] = {
            "broj_karte": sledeci_broj_karte,
            "putnici": putnici,
            "sifra_konkretnog_leta": sifra_konkretnog_leta,
            # "status": konstante.STATUS_NEREALIZOVANA_KARTA,
            "kupac": kupac,
            "prodavac": kwargs['prodavac'],
            "datum_prodaje": kwargs['datum_prodaje'],
            "obrisana": False
        }
        # return sve_karte
        return sve_karte[sledeci_broj_karte], sve_karte


def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: iter):
    lista = []
    for karta in range(len(sve_karte)):
        if sve_karte[karta]['status'] == konstante.STATUS_NEREALIZOVANA_KARTA:
            for putnik in range(len(sve_karte[karta]['putnici'])):
                if sve_karte[karta]['putnici'][putnik] == korisnik:
                    lista.append(sve_karte[karta])
    return lista


"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""


def izmena_karte(
        sve_karte: iter,
        svi_konkretni_letovi: iter,
        broj_karte: int,
        nova_sifra_konkretnog_leta: int = None,
        nov_datum_polaska:
        datetime = None,
        sediste=None
) -> dict:
    if nova_sifra_konkretnog_leta not in svi_konkretni_letovi.keys() and nova_sifra_konkretnog_leta is not None:
        raise AssertionError('Nepostojeci konkretni let')
    sve_karte.pop(broj_karte)
    sve_karte[sledeci_broj_karte] = {
        "broj_karte": sledeci_broj_karte,
        # "putnici": iter,
        "sifra_konkretnog_leta": nova_sifra_konkretnog_leta,
        "status": konstante.STATUS_NEREALIZOVANA_KARTA,
        "obrisana": False,
        "datum_prodaje": nov_datum_polaska,
        # "prodavac": str,
        # "kupac": str,
        'sediste': sediste
    }
    return sve_karte


"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata.
"""


def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
        sve_karte[broj_karte]['obrisana'] = True
        return sve_karte
    if korisnik['uloga'] == konstante.ULOGA_ADMIN:
        sve_karte.pop(broj_karte)
        return sve_karte
    if sve_karte[broj_karte] not in sve_karte:
        raise AssertionError('Ne postoji trazena karta')
    else:
        raise ValueError('Podaci nisu validni')


"""
Funkcija vraća sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosleđen.
"""


def pretraga_prodatih_karata(sve_karte: dict, svi_letovi: dict, svi_konkretni_letovi: dict, polaziste: str = "",
                             odrediste: str = "", datum_polaska: datetime = "", datum_dolaska: str = "",
                             korisnicko_ime_putnika: str = "") -> list:
    lista = []
    for karta in sve_karte:
        sifra = sve_karte[karta]['sifra_konkretnog_leta']
        broj_leta = svi_konkretni_letovi[sifra]['broj_leta']
        if not svi_letovi[broj_leta]['sifra_polazisnog_aerodroma'] == polaziste and not polaziste == '':
            continue
        if not svi_letovi[broj_leta]['sifra_odredisnog_aerodorma'] == odrediste and not odrediste == '':
            continue
        if not svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'] == datum_polaska and not datum_polaska == '':
            continue
        if not svi_konkretni_letovi[sifra]['datum_i_vreme_dolaska'] == datum_dolaska and not datum_dolaska == '':
            continue
        if korisnicko_ime_putnika not in sve_karte[karta]['putnici'] and not korisnicko_ime_putnika == '':
            continue
        else:
            lista.append(sve_karte[karta])
    return lista


"""
Funkcija čuva sve karte u fajl na zadatoj putanji sa zadatim separatorom.
"""


def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    with open(putanja, 'w', newline='') as csvfile:
        karta = ["broj_karte", "sifra_konkretnog_leta", "kupac", "prodavac", "sediste", "datum_prodaje",
                 "obrisana", "status", "putnici"]
        writer = csv.DictWriter(csvfile, fieldnames=karta, delimiter=separator)
        writer.writeheader()
        for i in sve_karte.keys():
            writer.writerow(sve_karte[i])


"""
Funkcija učitava sve karte iz fajla sa zadate putanje sa zadatim separatorom.
"""


def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    sve_karte = {}
    with open(putanja, 'r', newline='') as csvfile:
        next(csvfile)
        row = csvfile.readline().split(separator)
        # putnici = [json.loads(idx.replace("'", '"')) for idx in row[8]]
        while not row[0] == '':
            obrisana = True if row[6] == 'True\n' else False
            sve_karte[int(row[0])] = {
                "broj_karte": int(row[0]),
                "sifra_konkretnog_leta": int(row[1]),
                "kupac": eval(row[2]),
                "prodavac": eval(row[3]),
                "sediste": row[4],
                "datum_prodaje": row[5],
                "obrisana": obrisana,
                "status": row[7],
                "putnici": list(eval(row[8]))
            }
            row = csvfile.readline().split(separator)
    return sve_karte
