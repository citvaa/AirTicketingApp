from korisnici import korisnici
from common import konstante
from letovi import letovi
from datetime import datetime, timedelta
from operator import itemgetter
from karte import karte
import distutils.util
import json
from konkretni_letovi import konkretni_letovi
from izvestaji import izvestaji
from aerodromi import aerodromi
from model_aviona import model_aviona
import random

meni = {
    1: 'Registracija',
    2: 'Prijava na sistem',
}

meni1 = {
    21: 'Prikaz svih aerodroma',
    22: 'Prikaz svih karata',
    23: 'Prikaz svih konkretnih letova',
    24: 'Prikaz svih korisnika',
    25: 'Prikaz svih letova',
    26: 'Prikaz svih modela aviona',
    1: 'Izlazak iz aplikacije',
    2: 'Pregled nerealizovanih letova',
    3: 'Pretraga letova',
    4: 'Višekriterijumska pretraga letova',
    5: 'Prikaz 10 najjeftinijih (po opadajućoj ceni) letova između zadatog polazišta i odredišta',
    6: 'Fleksibilni polasci',
    7: 'Odjava sa sistema'
}

meni_kupac = {
    8: 'Kupovina karata',
    9: 'Pregled nerealizovanih karata',
    10: 'Prijava na let (check-in)'
}


def print_meni_kupac():
    for key in meni_kupac.keys():
        print(key, '--', meni_kupac[key])


meni_prodavac = {
    8: 'Prodaja karata',
    9: 'Prijava na let (check-in)',
    10: 'Izmena karte',
    11: 'Brisanje karte',
    12: 'Pretraga prodatih karata'
}


def print_meni_prodavac():
    for key in meni_prodavac.keys():
        print(key, '--', meni_prodavac[key])


meni_menadzer = {
    8: 'Pretraga prodatih karata',
    9: 'Registracija novih prodavaca',
    10: 'Kreiranje letova',
    11: 'Izmena letova',
    12: 'Brisanje karata',
    13: 'Izvestavanje'
}


def print_meni_menadzer():
    for key in meni_menadzer.keys():
        print(key, '--', meni_menadzer[key])


def print_meni():
    for key in meni.keys():
        print(key, '--', meni[key])


def registracija():
    print('Korisnicko ime: ')
    korisnicko_ime = input()
    print('Lozinka: ')
    lozinka = input()
    print('Kontakt telefon: ')
    kontakt_telefon = input()
    print('Email: ')
    email = input()
    print('Ime: ')
    ime = input()
    print('Prezime: ')
    prezime = input()
    while True:
        print('Da li zelite da unesete informacije o pasosu, drzavljanstvu i polu?')
        print('1. Da')
        print('2. Ne')
        option = int(input())
        if option == 1:
            print('Pasos: ')
            pasos = input()
            print('Drzavljanstvo: ')
            drzavljanstvo = input()
            print('Pol: ')
            pol = input()
            korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK, '', korisnicko_ime, lozinka,
                                        ime,
                                        prezime, email, pasos, drzavljanstvo, kontakt_telefon, pol)
            break
        if option == 2:
            korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK, '', korisnicko_ime, lozinka,
                                        ime,
                                        prezime, email, '', '', kontakt_telefon, '')
            break
        else:
            print("Unesite broj: ")
    print('Registracija uspesna')


def print_meni1():
    for key in meni1.keys():
        print(key, '--', meni1[key])


def prijava_na_sistem():
    if not len(prijavljen_korisnik) == 0:
        raise AssertionError('Vec je ulgovan korisnik')
    print('Korisnicko ime: ')
    korisnicko_ime = input()
    print('Lozinka: ')
    lozinka = input()
    korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
    print('Uspesan login')
    prijavljen_korisnik.append(svi_korisnici[korisnicko_ime])


def pregled_nerealizovanih_letova():
    print(*letovi.pregled_nerealizovanih_letova(svi_letovi), sep='\n')


def pretraga_letova():
    print('Polaziste: ')
    polaziste = input()
    print('Odrediste: ')
    odrediste = input()
    print('Datum polaska: (u formatu Y-m-d H:M:S)')
    datum_polaska = input()
    datum_polaska = datetime.strptime(datum_polaska, '%Y-%m-%d %H:%M:%S')
    print('Datum dolaska: (u formatu Y-m-d H:M:S)')
    datum_dolaska = input()
    datum_dolaska = datetime.strptime(datum_dolaska, '%Y-%m-%d %H:%M:%S')
    print('Vreme poletanja: ')
    vreme_poletanja = input()
    print('Vreme sletanja: ')
    vreme_sletanja = input()
    print('Prevoznik: ')
    prevoznik = input()
    print(*letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska,
                                  vreme_poletanja, vreme_sletanja, prevoznik), sep='\n')


kriterijumi_pretrage = {
    1: 'Polaziste',
    2: 'Odrediste',
    3: 'Datum polaska',
    4: 'Datum dolaska',
    5: 'Vreme poletanja',
    6: 'Vreme sletanja',
    7: 'Prevoznik',
    8: 'Kraj'
}


def print_kriterijumi_pretrage():
    for key in kriterijumi_pretrage.keys():
        print(key, '--', kriterijumi_pretrage[key])


def visekriterijumska_pretraga_letova():
    # inicijalne vrednosti
    polaziste = ''
    odrediste = ''
    datum_polaska = None
    datum_dolaska = None
    vreme_poletanja = ''
    vreme_sletanja = ''
    prevoznik = ''
    while True:
        print('Izaberite kriterijume pretrage:')
        print_kriterijumi_pretrage()
        option = int(input('Unesi broj: '))
        if option == 1:
            print('Polaziste: ')
            polaziste = input()
        elif option == 2:
            print('Odrediste: ')
            odrediste = input()
        elif option == 3:
            print('Datum polaska: ')
            datum_polaska = input()
            datum_polaska = datetime.strptime(datum_polaska, '%Y-%m-%d %H:%M:%S')
        elif option == 4:
            print('Datum dolaska: ')
            datum_dolaska = input()
            datum_dolaska = datetime.strptime(datum_dolaska, '%Y-%m-%d %H:%M:%S')
        elif option == 5:
            print('Vreme poletanja: ')
            vreme_poletanja = input()
        elif option == 6:
            print('Vreme sletanja: ')
            vreme_sletanja = input()
        elif option == 7:
            print('Prevoznik: ')
            prevoznik = input()
        elif option == 8:
            print(
                *letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska,
                                        datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik), sep='\n')
            return


def prikaz_10_najjeftinijih_letova():
    print('Polaziste:')
    polaziste = input()
    print('Odrediste:')
    odrediste = input()
    print(*letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste), sep='\n')


def sortiranje_liste_konkretnih_letova_po_ceni_opadajuce(svi_letovi, lista):
    for i in range(len(lista)):
        let = lista[i]
        broj_leta = let['broj_leta']
        let['cena'] = svi_letovi[broj_leta]['cena']
    lista = sorted(lista, key=itemgetter('cena'))
    lista.reverse()
    for i in range(len(lista)):
        let = lista[i]
        del let['cena']


def fleksibilni_polasci():
    print('Polaziste:')
    polaziste = input()
    print('Odrediste:')
    odrediste = input()
    print('Datum polaska:  (u formatu Y-m-d)')
    datum_polaska = input()
    datum_polaska = datetime.strptime(datum_polaska, '%Y-%m-%d').date()
    print('Datum dolaska:  (u formatu Y-m-d)')
    datum_dolaska = input()
    datum_dolaska = datetime.strptime(datum_dolaska, '%Y-%m-%d').date()
    print('Broj fleksibilnih dana')
    broj_fleksibilnih_dana = int(input())
    lista = letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska,
                                       broj_fleksibilnih_dana, datum_dolaska)
    sortiranje_liste_konkretnih_letova_po_ceni_opadajuce(svi_letovi, lista)
    print(*lista, sep='\n')


def kupovina_karata():
    prodavci = []
    for korisnik in svi_korisnici:
        if svi_korisnici[korisnik]['uloga'] == konstante.ULOGA_PRODAVAC:
            prodavci.append(svi_korisnici[korisnik])
    # a
    while True:
        print('Izaberite let pretragom ili unosom sifre:')
        print('1. Pretraga letova')
        print('2. Sifra konkretnog leta')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            pretraga_letova()
            print('Unesite sifru konkretnog leta: ')
            sifra = int(input())
            break
        elif option == 2:
            print('Unesite sifru konkretnog leta: ')
            sifra = int(input())
            break
        else:
            print('Unesite broj: ')
    zauzetost = svi_konkretni_letovi[sifra]['zauzetost']
    slobodna_mesta = 0
    for red in range(len(zauzetost)):
        for mesto in range(len(zauzetost[red])):
            if not zauzetost[red][mesto]:
                slobodna_mesta += 1
    if slobodna_mesta == 0:
        print('Nema slobodnih mesta')
        return

    # b
    putnici = []
    saputnik_da_li = 0
    while True:
        print('Da li kupujete kartu za')
        print('1. Sebe')
        print('2. Jos nekoga')
        option = int(input())
        if option == 1:
            break
        elif option == 2:
            saputnik_da_li += 1
            print('Unesite ime i prezime osobe kojoj kupujete kartu')
            print('Ime: ')
            ime = input()
            print('Prezime: ')
            prezime = input()
            saputnik = {'ime': ime, 'prezime': prezime}
            putnici.append(saputnik)
            break
        else:
            print('Unesite broj: ')
    # podaci o kontakt osobi
    ime = prijavljen_korisnik[0]['ime']
    prezime = prijavljen_korisnik[0]['prezime']
    korisnicko_ime = prijavljen_korisnik[0]['korisnicko_ime']
    email = prijavljen_korisnik[0]['email']
    telefon = prijavljen_korisnik[0]['telefon']
    putnik = {'ime': ime, 'prezime': prezime}
    putnici.append(putnik)

    # c
    if korisnicko_ime not in svi_korisnici.keys():
        korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK, '', korisnicko_ime, '', ime,
                                    prezime,
                                    email, '', '', telefon, '')
    kupac = svi_korisnici[korisnicko_ime]
    karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra, putnici, zauzetost, kupac, prodavac=random.choice(prodavci), datum_prodaje=datetime.now())
    print('Uspesna kupovina karte')

    # d
    # d1
    while True:
        print('Da li zelite da kupite kartu za povezan let?')
        print('1. Da')
        print('2. Ne')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            print('Povezani letovi:')
            print(*letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[sifra]), sep='\n')
            print('Unesite sifru novog leta: ')
            sifra2 = int(input())
            zauzetost2 = svi_konkretni_letovi[sifra2]['zauzetost']
            karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra2, [putnik], zauzetost2, kupac, prodavac=random.choice(prodavci), datum_prodaje=datetime.now())
            print('Uspesna kupovina karte')
            # d2
            if not saputnik_da_li == 0:
                while True:
                    print('Da li zelite da kupite kartu za povezan let i za saputnika?')
                    print('1. Da')
                    print('2. Ne')
                    print('Unesite broj: ')
                    option = int(input())
                    if option == 1:
                        if slobodna_mesta < 2:
                            print('Nema slobodnih mesta za saputnika')
                            return
                        else:
                            karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra2, [saputnik], zauzetost2, kupac, prodavac=random.choice(prodavci), datum_prodaje=datetime.now())
                            print('Uspesna kupovina')
                            return
                    if option == 2:
                        return
                    else:
                        print('Unesite broj: ')
            break
        elif option == 2:
            return
        else:
            print('Unesite broj: ')


def odjava_sa_sistema():
    if not len(prijavljen_korisnik) == 0:
        prijavljen_korisnik.clear()
        korisnici.logout(prijavljen_korisnik[0]['korisnicko_ime'])
    else:
        print('Niko nije prijavljen')


def pregled_nerealizovanih_karata():
    print(*karte.pregled_nerealizovanaih_karata(prijavljen_korisnik[0], sve_karte), sep='\n')


def prijava_na_let():
    while True:
        print('Unesite broj karte')
        print('1. Pomocu pretrage')
        print('2. Direktnim unosom')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            pregled_nerealizovanih_karata()
            print('Unesite broj karte: ')
            broj_karte = int(input())
            break
        if option == 2:
            print('Unesite broj karte: ')
            broj_karte = int(input())
            break
        else:
            print('Unesite broj: ')
    if prijavljen_korisnik[0]['pasos'] == '':
        print('Unesite broj pasosa: ')
        pasos = input()
        print('Unesite drzavljanstvo: ')
        drzavljanstvo = input()
        print('Unesite pol: ')
        pol = input()
    sifra_leta = sve_karte[broj_karte]['sifra_konkretnog_leta']
    print('Dostupna sedista:')
    # letovi.podesi_matricu_zauzetosti(svi_letovi, svi_konkretni_letovi[sifra_leta])
    print(*letovi.matrica_zauzetosti(svi_konkretni_letovi[sifra_leta]), sep='\n')
    print('Izaberite red: (0-' + str(
        svi_letovi[svi_konkretni_letovi[sifra_leta]['broj_leta']]['model']['broj_redova']) + ')')
    red = int(input())
    print('Izaberite poziciju: (' + str(
        svi_letovi[svi_konkretni_letovi[sifra_leta]['broj_leta']]['model']['pozicije_sedista']) + ')')
    pozicija = input()
    letovi.checkin(sve_karte[broj_karte], svi_letovi, svi_konkretni_letovi[sifra_leta], red, pozicija)
    print('Checkin uspesan')
    while True:
        print('Da li zelite da uradite checkin i za povezane letove?')
        print('1. Da')
        print('2. Ne')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            while True:
                print('Prikaz povezanih letova:')
                print(*letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[sifra_leta]),
                      sep='\n')
                print('Unesite broj leta')
                print('1. Pomocu pretrage')
                print('2. Direktnim unosom')
                print('Unesite broj: ')
                option = int(input())
                if option == 1:
                    pregled_nerealizovanih_karata()
                    print('Unesite broj karte: ')
                    broj_karte2 = int(input())
                    break
                if option == 2:
                    print('Unesite broj karte: ')
                    broj_karte2 = int(input())
                    break
                else:
                    print('Unesite broj: ')
            sifra_leta2 = sve_karte[broj_karte]['sifra_konkretnog_leta']
            print('Dostupna sedista:')
            print(*letovi.matrica_zauzetosti(svi_konkretni_letovi[sifra_leta2]), sep='\n')
            print('Izaberite red: (0-' + str(
                svi_letovi[svi_konkretni_letovi[sifra_leta2]['broj_leta']]['model']['broj_redova']) + ')')
            red2 = int(input())
            print('Izaberite poziciju: (' + str(
                svi_letovi[svi_konkretni_letovi[sifra_leta2]['broj_leta']]['model']['pozicije_sedista']) + ')')
            pozicija2 = input()
            letovi.checkin(sve_karte[broj_karte2], svi_letovi, svi_konkretni_letovi[sifra_leta2], red2, pozicija2)
            print('Checkin uspesan')
            break
        elif option == 2:
            break
        else:
            print('Unesite broj:')
    while True:
        print('Da li zelite da unesete potrebne podatke za saputnike?')
        print('1. Da')
        print('2. Ne')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            while True:
                print('Unesite broj karte')
                print('1. Pomocu pretrage')
                print('2. Direktnim unosom')
                print('Unesite broj: ')
                option = int(input())
                if option == 1:
                    pregled_nerealizovanih_karata()
                    print('Unesite broj karte: ')
                    broj_karte3 = int(input())
                    break
                if option == 2:
                    print('Unesite broj karte: ')
                    broj_karte3 = int(input())
                    break
                else:
                    print('Unesite broj: ')
            sifra_leta3 = sve_karte[broj_karte]['sifra_konkretnog_leta']
            print('Dostupna sedista:')
            print(*letovi.matrica_zauzetosti(svi_konkretni_letovi[sifra_leta3]), sep='\n')
            print('Izaberite red: (0-' + str(
                svi_letovi[svi_konkretni_letovi[sifra_leta3]['broj_leta']]['model']['broj_redova']) + ')')
            red3 = int(input())
            print('Izaberite poziciju: (' + str(
                svi_letovi[svi_konkretni_letovi[sifra_leta3]['broj_leta']]['model']['pozicije_sedista']) + ')')
            pozicija3 = input()
            letovi.checkin(sve_karte[broj_karte3], svi_letovi, svi_konkretni_letovi[sifra_leta3], red3, pozicija3)
            print('Checkin uspesan')
            break
        elif option == 2:
            break
        else:
            print('Unesite broj: ')


def prodaja_karte():
    # a
    while True:
        print('Izaberite zeljeni konkretni let preko:')
        print('1. Pretraga letova')
        print('2. Sifra konkretnog leta')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            pretraga_letova()
            print('Unesite sifru konkretnog leta: ')
            sifra = int(input())
            break
        elif option == 2:
            print('Unesite sifru konkretnog leta: ')
            sifra = int(input())
            break
        else:
            print('Unesite broj: ')
    zauzetost = svi_konkretni_letovi[sifra]['zauzetost']
    slobodna_mesta = 0
    for red in range(len(zauzetost)):
        for mesto in range(len(zauzetost[red])):
            if not zauzetost[red][mesto]:
                slobodna_mesta += 1
    if slobodna_mesta == 0:
        print('Nema slobodnih mesta')
        return

    # b
    putnici = []
    while True:
        print('Kupac je: ')
        print('1. Registrovan')
        print('2. Neregistrovan')
        print('Unesi broj: ')
        option = int(input())
        if option == 1:
            print('Unesi korisnicko ime kupca')
            korisnicko_ime = input()
            kupac = svi_korisnici[korisnicko_ime]
            break
        if option == 2:
            print('Unesite informacije o kupcu: ')
            print('Korisnicko ime: ')
            korisnicko_ime = input()
            print('Ime: ')
            ime = input()
            print('Prezime: ')
            prezime = input()
            print('Telefon: ')
            telefon = input()
            print('Email: ')
            email = input()
            korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK, '', korisnicko_ime, '', ime,
                                        prezime, email, '', '', telefon, '')
            kupac = svi_korisnici[korisnicko_ime]
            break
        else:
            print('Unesi broj: ')

    # c
    zauzetost = svi_konkretni_letovi[sifra]['zauzetost']
    karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra, putnici, zauzetost, kupac, prodavac=prijavljen_korisnik[0], datum_prodaje=datetime.now())
    print('Uspesna prodaja karte')

    # d1
    while True:
        print('Da li zelite da prodate kartu za povezan let?')
        print('1. Da')
        print('2. Ne')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            print(*letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[sifra]), sep='\n')
            print('Unesite sifru novog leta: ')
            sifra2 = int(input())
            zauzetost2 = svi_konkretni_letovi[sifra2]['zauzetost']
            karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra2, [kupac], zauzetost2, kupac, prodavac=prijavljen_korisnik[0], datum_prodaje=datetime.now())
            print('Uspesna prodaja karte')
            # d2
            while True:
                print('Da li zelite da prodate kartu za povezan let i za saputnika?')
                print('1. Da')
                print('2. Ne')
                print('Unesite broj: ')
                option = int(input())
                if option == 1:
                    if slobodna_mesta < 2:
                        print('Nema slobodnih mesta za saputnika')
                        return
                    else:
                        print('Unesite podatke saputnika: ')
                        print('Ime: ')
                        ime = input()
                        print('Prezime')
                        prezime = input()
                        saputnik = {'ime': ime, 'prezime': prezime}
                        karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra2, [saputnik], zauzetost2, kupac, prodavac=prijavljen_korisnik[0], datum_prodaje=datetime.now())
                        print('Uspesna prodaja')
                        return
                if option == 2:
                    return
                else:
                    print('Unesite broj: ')
        elif option == 2:
            break
        else:
            print('Unesite broj: ')


def izmena_karte():
    while True:
        print('Unesite broj karte')
        print('1. Pomocu pretrage')
        print('2. Direktnim unosom')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            pregled_nerealizovanih_karata()
            print('Unesite broj karte: ')
            broj_karte = int(input())
            break
        if option == 2:
            print('Unesite broj karte: ')
            broj_karte = int(input())
            break
        else:
            print('Unesite broj: ')
    sifra_leta = sve_karte[broj_karte]['sifra_konkretnog_leta']
    # postavljanje defaultnih vrednosti
    nova_sifra_konkretnog_leta = sifra_leta
    nov_datum_polaska = svi_konkretni_letovi[sifra_leta]['datum_i_vreme_polaska']
    sediste = sve_karte[broj_karte]['sediste']
    while True:
        print('Izaberi stavke za menjanje:')
        print('1. Sifra leta')
        print('2. Datum polaska')
        print('3. Sediste')
        print('4. Kraj')
        print('Unesite broj:')
        option = int(input())
        if option == 1:
            print('Nova sifra leta: ')
            nova_sifra_konkretnog_leta = int(input())
        if option == 2:
            print('Nov datum polaska: ')
            datum_polaska = input()
            nov_datum_polaska = datetime.strptime(datum_polaska, '%Y-%m-%d %H:%M:%S')
        if option == 3:
            print('Novo sediste: ')
            sediste = input()
        if option == 4:
            break
    karte.izmena_karte(sve_karte, svi_konkretni_letovi, broj_karte, nova_sifra_konkretnog_leta, nov_datum_polaska,
                       sediste)
    print('Uspesna izmena karte')


def brisanje_karte():
    while True:
        print('Unesite broj karte')
        print('1. Pomocu pretrage')
        print('2. Direktnim unosom')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            pregled_nerealizovanih_karata()
            print('Unesite broj karte: ')
            broj_karte = int(input())
            break
        if option == 2:
            print('Unesite broj karte: ')
            broj_karte = int(input())
            break
        else:
            print('Unesite broj: ')
    sve_karte[broj_karte]['obrisana'] = True
    print('Karta oznacena kao obrisana. Ceka se dozvola menadzera za trajno brisanje')


def pretraga_prodatih_karata():
    # postavljanje defaultnih vrednosti
    polaziste = ''
    odrediste = ''
    datum_polaska = ''
    datum_dolaska = ''
    korisnicko_ime = ''
    while True:
        print('Izaberite parametre pretrazivanja:')
        print('1. Polaziste')
        print('2. Odrediste')
        print('3. Datum polaska')
        print('4. Datum dolaska')
        print('5. Korisnicko ime putnika')
        print('6. Kraj')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            print('Unesite polaziste: ')
            polaziste = input()
        if option == 2:
            print('Unesite odrediste: ')
            odrediste = input()
        if option == 3:
            print('Unesite datum polaska')
            datum_polaska = input()
            datum_polaska = datetime.strptime(datum_polaska, '%Y-%m-%d %H:%M:%S')
        if option == 4:
            print('Unesite datum dolaska')
            datum_dolaska = input()
            datum_dolaska = datetime.strptime(datum_dolaska, '%Y-%m-%d %H:%M:%S')
        if option == 5:
            print('Unesite ime i prezime putnika')
            print('Ime: ')
            ime = input()
            print('Prezime: ')
            prezime = input()
            for korisnik in svi_korisnici:
                if svi_korisnici[korisnik]['ime'] == ime and svi_korisnici[korisnik]['prezime'] == prezime:
                    korisnicko_ime = korisnik
        if option == 6:
            break
    print(
        *karte.pretraga_prodatih_karata(sve_karte, svi_letovi, svi_konkretni_letovi, polaziste, odrediste,
                                        datum_polaska,
                                        datum_dolaska, korisnicko_ime), sep='\n')


def registracija_novih_prodavaca():
    print('Unesite podatke prodavca')
    print('Korisnicko ime: ')
    korisnicko_ime = input()
    print('Lozinka: ')
    lozinka = input()
    print('Kontakt telefon: ')
    kontakt_telefon = input()
    print('Email: ')
    email = input()
    print('Ime: ')
    ime = input()
    print('Prezime: ')
    prezime = input()
    while True:
        print('Da li zelite da unesete informacije o pasosu, drzavljanstvu i polu?')
        print('1. Da')
        print('2. Ne')
        option = int(input())
        if option == 1:
            print('Pasos: ')
            pasos = input()
            print('Drzavljanstvo: ')
            drzavljanstvo = input()
            print('Pol: ')
            pol = input()
            korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_PRODAVAC, '', korisnicko_ime, lozinka,
                                        ime,
                                        prezime, email, pasos, drzavljanstvo, kontakt_telefon, pol)
            break
        if option == 2:
            korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_PRODAVAC, '', korisnicko_ime, lozinka,
                                        ime,
                                        prezime, email, '', '', kontakt_telefon, '')
            break
        else:
            print("Unesite broj: ")
    print('Registracija uspesna')


def kreiranje_letova():
    print('Unesite podatke o letu:')
    print('Broj leta: (u obliku <slovo><slovo><cifra><cifra>)')
    broj_leta = input()
    print('Polaziste: ')
    polaziste = input()
    print('Odrediste: ')
    odrediste = input()
    print('Vreme poletanja: ')
    vreme_poletanja = input()
    print('Vreme sletanja: ')
    vreme_sletanja = input()
    print('Sletanje sutra (y/n): ')
    sletanje_sutra = input()
    sletanje_sutra = distutils.util.strtobool(sletanje_sutra)
    sletanje_sutra = bool(sletanje_sutra)
    print('Prevoznik: ')
    prevoznik = input()
    print('Dani: ')
    dani = list(input())
    print('Model: ')
    model = input()
    model = eval(model)
    print('Cena: ')
    cena = float(input())
    print('Datum pocetka operativnosti: (u formatu Y-m-d H:M:S)')
    datum_pocetka_operativnosti = input()
    datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, '%Y-%m-%d %H:%M:%S')
    print('Datum kraja operativnosti: (u formatu Y-m-d H:M:S)')
    datum_kraja_operativnosti = input()
    datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, '%Y-%m-%d %H:%M:%S')
    letovi.kreiranje_letova(svi_letovi, broj_leta, polaziste, odrediste, vreme_poletanja, vreme_sletanja,
                            sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti,
                            datum_kraja_operativnosti)
    konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi, svi_letovi[broj_leta])
    print('Uspesno kreiran let i njegovi konkretni letovi')


def izmena_letova():
    while True:
        print('Unesite broj leta')
        print('1. Pomocu pretrage')
        print('2. Direktnim unosom')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            pregled_nerealizovanih_letova()
            print('Unesite broj leta: ')
            broj_leta = input()
            break
        if option == 2:
            print('Unesite broj leta: ')
            broj_leta = input()
            break
        else:
            print('Unesite broj: ')

    # postavljanje defaultnih vrednosti
    let = svi_letovi[broj_leta]
    polaziste = let['sifra_polazisnog_aerodroma']
    odrediste = let['sifra_odredisnog_aerodorma']
    vreme_poletanja = let['vreme_poletanja']
    vreme_sletanja = let['vreme_sletanja']
    sletanje_sutra = bool(let['sletanje_sutra'])
    prevoznik = let['prevoznik']
    dani = let['dani']
    model = let['model']
    cena = let['cena']
    datum_pocetka_operativnosti = let['datum_pocetka_operativnosti']
    datum_kraja_operativnosti = let['datum_kraja_operativnosti']

    while True:
        print('Izaberite sta zelite da menjate:')
        print('1. Polaziste')
        print('2. Odrediste')
        print('3. Vreme poletanja')
        print('4. Vreme sletanja')
        print('5. Sletanje sutra')
        print('6. Prevoznik')
        print('7. Dani')
        print('8. Model')
        print('9. Cena')
        print('10. Datum pocetka operativnosti')
        print('11. Datum kraja operativnosti')
        print('12. Kraj')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            print('Unesite polaziste: ')
            polaziste = input()
        if option == 2:
            print('Unesite odrediste: ')
            odrediste = input()
        if option == 3:
            print('Unesite vreme poletanja: ')
            vreme_poletanja = input()
        if option == 4:
            print('Unesite vreme sletanja: ')
            vreme_sletanja = input()
        if option == 5:
            print('Unesite da li avion slece sutradan (y/n): ')
            sletanje_sutra = input()
            sletanje_sutra = distutils.util.strtobool(sletanje_sutra)
        if option == 6:
            print('Unesite prevoznika: ')
            prevoznik = input()
        if option == 7:
            print('Unesite dane: ')
            dani = list(input())
        if option == 8:
            print('Unesite model: ')
            model = input()
            model = json.loads(model)
        if option == 9:
            print('Unesite cenu: ')
            cena = float(input())
        if option == 10:
            print('Datum pocetka operativnosti: ')
            datum_pocetka_operativnosti = input()
            datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, '%Y-%m-%d %H:%M:%S')
        if option == 11:
            print('Datum kraja operativnosti: ')
            datum_kraja_operativnosti = input()
            datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, '%Y-%m-%d %H:%M:%S')
        if option == 12:
            break

    letovi.izmena_letova(svi_letovi, broj_leta, polaziste, odrediste, vreme_poletanja, vreme_sletanja, sletanje_sutra,
                         prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti)
    print('Uspesna izmena letova')


def brisanje_karata():
    karte_brisanje = {}  # recnik karata oznacenih za brisanje
    for karta in sve_karte:
        if sve_karte[karta]['obrisana']:
            broj_karte = sve_karte[karta]['broj_karte']
            karte_brisanje[broj_karte] = {sve_karte[karta]}
    # ispis karata oznacenih za brisanje
    print('Karte oznacene za brisanje:')
    print(karte_brisanje)
    print('1. Obrisi sve karte')
    print('2. Odaberi karte za brisanje')
    print('3. Odaberi karte za ponistenje brisanja')
    print('Unesi broj: ')
    option = int(input())
    if option == 1:
        for karta in karte_brisanje:
            sve_karte.pop(karta)
        print('Karte su obrisane')
    elif option == 2:
        for karta in karte_brisanje:
            print(karte_brisanje[karta])
            print('Da li zelite da obrisete ovu kartu? (y/n)')
            option = input()
            option = distutils.util.strtobool(option)
            if option:
                sve_karte.pop(karta)
                print('Karta je obrisana')
            else:
                continue
    elif option == 3:
        for karta in karte_brisanje:
            print(karte_brisanje[karta])
            print('Da li zelite da ponistite brisanje ove karte? (y/n)')
            option = input()
            option = distutils.util.strtobool(option)
            if option:
                sve_karte[karta]['obrisana'] = False
                print('Brisanje karte je ponisteno')
            else:
                continue


def izvestavanje():
    while True:
        print('Izaberite izvestaj:')
        print('1. Lista prodatih karata za izabrani dan prodaje')
        print('2. Lista prodatih karata za izabrani dan polaska')
        print('3. Lista prodatih karata za izabrani dan prodaje i izabranog prodavca')
        print('4. Ukupan broj i cena prodatih karata za izabrani dan prodaje')
        print('5. Ukupan broj i cena prodatih karata za izabrani dan polaska')
        print('6. Ukupan broj i cena prodatih karata za izabrani dan prodaje i izabranog prodavca')
        print('7. Ukupan broj i cena prodatih karata u poslednjih 30 dana, po prodavcima')
        print('8. Kraj')
        print('Unesite broj: ')
        option = int(input())
        if option == 1:
            print('Unesi dan prodaje: (u formatu d.m.Y.)')
            dan = input()
            # dan = datetime.strptime(dan, '%Y-%m-%d').date()
            print(*izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(sve_karte, dan), sep='\n')
        if option == 2:
            print('Unesi dan polaska: (u formatu Y-m-d)')
            dan = input()
            dan = datetime.strptime(dan, '%Y-%m-%d').date()
            print(*izvestaji.izvestaj_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, dan), sep='\n')
        if option == 3:
            print('Unesi dan prodaje: (u formatu d.m.Y.)')
            dan = input()
            # dan = datetime.strptime(dan, '%Y-%m-%d').date()
            print('Unesi ime prodavca: ')
            prodavac = input()
            # print(*izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, dan, prodavac), sep='\n')

            lista = []
            for karta in sve_karte:
                if sve_karte[karta]['datum_prodaje'] == dan and sve_karte[karta]['prodavac']['ime'] == prodavac:
                    lista.append(sve_karte[karta])
            print(*lista, sep='\n')
        if option == 4:
            print('Unesi dan prodaje: (u formatu d.m.Y.)')
            dan = input()
            # dan = datetime.strptime(dan, '%Y-%m-%d').date()
            print(
                *izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte, svi_konkretni_letovi, svi_letovi,
                                                                       dan), sep='\n')
        if option == 5:
            print('Unesi dan polaska: (u formatu Y-m-d H:S:S)')
            dan = input()
            dan = datetime.strptime(dan, '%Y-%m-%d %H:%M:%S')
            print(
                *izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, svi_letovi,
                                                                       dan), sep='\n')
        if option == 6:
            print('Unesi dan prodaje: (u formatu d.m.Y.)')
            dan = input()
            # dan = datetime.strptime(dan, '%Y-%m-%d').date()
            print('Unesi ime prodavca: ')
            prodavac = input()
            # print(*izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, svi_konkretni_letovi,
            #                                                                         svi_letovi, dan, prodavac),
            #       sep='\n')

            broj = 0
            cena = 0
            for karta in sve_karte:
                if sve_karte[karta]['datum_prodaje'] == dan and sve_karte[karta]['prodavac']['ime'] == prodavac:
                    broj += 1
                    sifra_konkretnog_leta = sve_karte[karta]['sifra_konkretnog_leta']
                    broj_leta = svi_konkretni_letovi[sifra_konkretnog_leta]['broj_leta']
                    cena += svi_letovi[broj_leta]['cena']
            tapl = (broj, cena)
            print(*tapl, sep='\n')

        if option == 7:
            # print(*izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte, svi_konkretni_letovi,
            #                                                                     svi_letovi), sep='\n')

            broj = 0
            cena = 0
            izvestaj = {}
            for karta in sve_karte:
                if datetime.today().date() >= datetime.strptime(sve_karte[karta]['datum_prodaje'],
                                                                '%d.%m.%Y.').date() >= (
                        datetime.today().date() - timedelta(days=30)):
                    broj += 1
                    cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]['sifra_konkretnog_leta']]['broj_leta']][
                        'cena']
                    if sve_karte[karta]['prodavac']['ime'] in izvestaj.keys():
                        izvestaj[sve_karte[karta]['prodavac']['ime']]['broj'] += broj
                        izvestaj[sve_karte[karta]['prodavac']['ime']]['cena'] += cena
                    else:
                        izvestaj[sve_karte[karta]['prodavac']['ime']] = {
                            'broj': broj,
                            'cena': cena
                        }
            ispis_recnika(izvestaj)
        if option == 8:
            break


def ispis_recnika(recnik: dict):
    for key, value in recnik.items():
        print(key, ' : ', value)


if __name__ == '__main__':
    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla('korisnici.csv', ',')
    svi_aerodromi = aerodromi.ucitaj_aerodrom('aerodromi.csv', ',')
    svi_modeli_aviona = model_aviona.ucitaj_modele_aviona('modeli_aviona.csv', ',')
    svi_letovi = letovi.ucitaj_letove_iz_fajla('letovi.csv', ';')
    svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let('konkretni_letovi.csv', '/')
    sve_karte = karte.ucitaj_karte_iz_fajla('karte.csv', '|')
    prijavljen_korisnik = []
    while True:
        print_meni()
        option = int(input('Unesi broj: '))
        if option == 1:
            registracija()
        elif option == 2:
            if len(prijavljen_korisnik) == 0:
                prijava_na_sistem()
                while True:
                    print_meni1()
                    if prijavljen_korisnik[0]['uloga'] == konstante.ULOGA_KORISNIK:
                        print_meni_kupac()
                        option = int(input('Unesi broj: '))
                        if option == 21:
                            ispis_recnika(svi_aerodromi)
                        elif option == 22:
                            ispis_recnika(sve_karte)
                        elif option == 23:
                            ispis_recnika(svi_konkretni_letovi)
                        elif option == 24:
                            ispis_recnika(svi_korisnici)
                        elif option == 25:
                            ispis_recnika(svi_letovi)
                        elif option == 26:
                            ispis_recnika(svi_modeli_aviona)
                        elif option == 1:
                            exit()
                        elif option == 2:
                            pregled_nerealizovanih_letova()
                        elif option == 3:
                            pretraga_letova()
                        elif option == 4:
                            visekriterijumska_pretraga_letova()
                        elif option == 5:
                            prikaz_10_najjeftinijih_letova()
                        elif option == 6:
                            fleksibilni_polasci()
                        elif option == 7:
                            odjava_sa_sistema()
                            break
                        elif option == 8:
                            kupovina_karata()
                        elif option == 9:
                            pregled_nerealizovanih_karata()
                        elif option == 10:
                            prijava_na_let()
                    elif prijavljen_korisnik[0]['uloga'] == konstante.ULOGA_PRODAVAC:
                        print_meni_prodavac()
                        option = int(input('Unesi broj: '))
                        if option == 21:
                            ispis_recnika(svi_aerodromi)
                        elif option == 22:
                            ispis_recnika(sve_karte)
                        elif option == 23:
                            ispis_recnika(svi_konkretni_letovi)
                        elif option == 24:
                            ispis_recnika(svi_korisnici)
                        elif option == 25:
                            ispis_recnika(svi_letovi)
                        elif option == 26:
                            ispis_recnika(svi_modeli_aviona)
                        elif option == 1:
                            exit()
                        elif option == 2:
                            pregled_nerealizovanih_letova()
                        elif option == 3:
                            pretraga_letova()
                        elif option == 4:
                            visekriterijumska_pretraga_letova()
                        elif option == 5:
                            prikaz_10_najjeftinijih_letova()
                        elif option == 6:
                            fleksibilni_polasci()
                        elif option == 7:
                            odjava_sa_sistema()
                            break
                        elif option == 8:
                            prodaja_karte()
                        elif option == 9:
                            prijava_na_let()
                        elif option == 10:
                            izmena_karte()
                        elif option == 11:
                            brisanje_karte()
                        elif option == 12:
                            pretraga_prodatih_karata()
                    elif prijavljen_korisnik[0]['uloga'] == konstante.ULOGA_ADMIN:
                        print_meni_menadzer()
                        option = int(input('Unesi broj: '))
                        if option == 21:
                            ispis_recnika(svi_aerodromi)
                        elif option == 22:
                            ispis_recnika(sve_karte)
                        elif option == 23:
                            ispis_recnika(svi_konkretni_letovi)
                        elif option == 24:
                            ispis_recnika(svi_korisnici)
                        elif option == 25:
                            ispis_recnika(svi_letovi)
                        elif option == 26:
                            ispis_recnika(svi_modeli_aviona)
                        elif option == 1:
                            exit()
                        elif option == 2:
                            pregled_nerealizovanih_letova()
                        elif option == 3:
                            pretraga_letova()
                        elif option == 4:
                            visekriterijumska_pretraga_letova()
                        elif option == 5:
                            prikaz_10_najjeftinijih_letova()
                        elif option == 6:
                            fleksibilni_polasci()
                        elif option == 7:
                            odjava_sa_sistema()
                            break
                        elif option == 8:
                            pretraga_prodatih_karata()
                        elif option == 9:
                            registracija_novih_prodavaca()
                        elif option == 10:
                            kreiranje_letova()
                        elif option == 11:
                            izmena_letova()
                        elif option == 12:
                            brisanje_karata()
                        elif option == 13:
                            izvestavanje()
            else:
                print('Korisnik je vec ulogovan. Morate se prvo odjaviti')
        else:
            print('Los unos. Probajte opet.')
