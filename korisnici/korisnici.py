import common.konstante
from common import konstante
import re
import csv

"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni.
    Hint: Postoji string funkcija koja proverava da li je string broj bez bacanja grešaka. Probajte da je pronađete.
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""


def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str,
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", pol: str = "") -> dict:
    # kreiranje novog korisnika

    if not azuriraj:
        temp = 0
        for i in svi_korisnici:
            if i == korisnicko_ime:
                temp += 1
        if temp != 0:
            raise ValueError('Korisnicko ime je zauzeto.')

        # provera unetih podataka

        regex = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Z|a-z]{2,}$'

        if uloga != konstante.ULOGA_KORISNIK and uloga != konstante.ULOGA_PRODAVAC and uloga != konstante.ULOGA_ADMIN:
            raise ValueError('Greska. Niste izabrali mogucu ulogu korisnika')
        if not type(staro_korisnicko_ime) == str:
            raise ValueError('Greska. Staro korisnicko ime mora biti tipa string')
        if not type(korisnicko_ime) == str:
            raise ValueError('Greska. Korisnicko ime mora biti tipa string')
        if not type(lozinka) == str:
            raise ValueError('Greska. Lozinka mora biti tipa string')
        if not type(ime) == str:
            raise ValueError('Greska. Ime mora biti tipa string')
        if not type(prezime) == str:
            raise ValueError('Greska. Prezime mora biti tipa string')
        if (not type(email) == str or not re.match(regex, email)) and email != '':
            raise ValueError('Greska. Email mora biti tipa string u obliku ime@domen (npr. primer@email.com)')
        if (not type(pasos) == str or len(pasos) != 9 or not pasos.isnumeric()) and pasos != '':
            raise ValueError('Greska. Pasos mora biti tipa string od 9 cifara')
        if not type(drzavljanstvo) == str:
            raise ValueError('Greska. Drzavljanstvo mora biti tipa string')
        if (not type(telefon) == str or not telefon.isnumeric()) and telefon != '':
            raise ValueError('Greska. Telefon mora sadrzati samo cifre i biti tipa string')
        if not type(pol) == str:
            raise ValueError('Greska. Pol mora biti tipa string')
        else:
            svi_korisnici[korisnicko_ime] = {
                "ime": ime,
                "prezime": prezime,
                "korisnicko_ime": korisnicko_ime,
                "lozinka": lozinka,
                "email": email,
                "pasos": pasos,
                "drzavljanstvo": drzavljanstvo,
                "telefon": telefon,
                "pol": pol,
                "uloga": uloga
            }
            return svi_korisnici

    # azuriranje korisnika

    else:
        temp1 = 0
        for i in svi_korisnici:
            if i == staro_korisnicko_ime:
                temp1 += 1
            if i == korisnicko_ime and korisnicko_ime != staro_korisnicko_ime:
                raise ValueError('Greska. Korisnicko ime je zauzeto')
        if temp1 == 0:
            raise ValueError('Greska. Ne postoji trazeni korisnik')

    # provera unetih podataka

    regex = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Z|a-z]{2,}$'

    if uloga != konstante.ULOGA_KORISNIK and uloga != konstante.ULOGA_PRODAVAC and uloga != konstante.ULOGA_ADMIN:
        raise ValueError('Greska. Niste izabrali mogucu ulogu korisnika')
    if not type(staro_korisnicko_ime) == str:
        raise ValueError('Greska. Staro korisnicko ime mora biti tipa string')
    if not type(korisnicko_ime) == str:
        raise ValueError('Greska. Korisnicko ime mora biti tipa string')
    if not type(lozinka) == str:
        raise ValueError('Greska. Lozinka mora biti tipa string')
    if not type(ime) == str:
        raise ValueError('Greska. Ime mora biti tipa string')
    if not type(prezime) == str:
        raise ValueError('Greska. Prezime mora biti tipa string')
    if (not type(email) == str or not re.match(regex, email)) and email != '':
        raise ValueError('Greska. Email mora biti tipa string u obliku ime@domen (npr. primer@email.com)')
    if (not type(pasos) == str or len(pasos) != 9 or not pasos.isnumeric()) and pasos != '':
        raise ValueError('Greska. Pasos mora biti tipa string od 9 cifara')
    if not type(drzavljanstvo) == str:
        raise ValueError('Greska. Drzavljanstvo mora biti tipa string')
    if (not type(telefon) == str or not telefon.isnumeric()) and telefon != '':
        raise ValueError('Greska. Telefon mora sadrzati samo cifre i biti tipa string')
    if not type(pol) == str:
        raise ValueError('Greska. Pol mora biti tipa string')
    else:
        svi_korisnici.pop(staro_korisnicko_ime)
        svi_korisnici[korisnicko_ime] = {
            "ime": ime,
            "prezime": prezime,
            "korisnicko_ime": korisnicko_ime,
            "lozinka": lozinka,
            "email": email,
            "pasos": pasos,
            "drzavljanstvo": drzavljanstvo,
            "telefon": telefon,
            "pol": pol,
            "uloga": uloga
        }
        return svi_korisnici


"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""


def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    with open(putanja, 'w', newline='') as csvfile:
        korisnik = ["uloga", "korisnicko_ime", "lozinka", "ime", "prezime", "email", "pasos", "drzavljanstvo",
                    "telefon", "pol"]
        writer = csv.DictWriter(csvfile, fieldnames=korisnik, delimiter=separator)
        writer.writeheader()
        for i in svi_korisnici.keys():
            writer.writerow(svi_korisnici[i])


"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""


def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator)
        svi_korisnici = {}
        for korisnik in reader:
            svi_korisnici[korisnik['korisnicko_ime']] = korisnik
        return svi_korisnici
    # svi_korisnici = {}
    # with open(putanja, 'r', newline='') as csvfile:
    #     next(csvfile)
    #     row = csvfile.readline().split(separator)
    #     while not row[0] == '':
    #         svi_korisnici[row[0]] = {
    #             "uloga": row[0],
    #             "korisnicko_ime": row[1],
    #             "lozinka": row[2],
    #             "ime": row[3],
    #             "prezime": row[4],
    #             "email": row[5],
    #             "pasos": row[6],
    #             "drzavljanstvo": row[7],
    #             "telefon": row[8],
    #             "pol": row[9]
    #         }
    #         row = csvfile.readline().split(separator)
    # return svi_korisnici


"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""


def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    for i in svi_korisnici:
        if i == korisnicko_ime and svi_korisnici.get(i).get('lozinka') == lozinka:
            return svi_korisnici[i]
    raise ValueError('Greska. Korisnik nije pronadjen')


"""
Funkcija koja vrsi log out
*
"""


def logout(korisnicko_ime: str):
    print('Korisnik ' + korisnicko_ime + ' je uspesno izlogovan')
