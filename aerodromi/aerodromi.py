import csv


"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""


def kreiranje_aerodroma(
        svi_aerodromi: dict,
        skracenica: str = "",
        pun_naziv: str = "",
        grad: str = "",
        drzava: str = ""
) -> dict:
    if skracenica == '' or pun_naziv == '' or grad == '' or drzava == '':
        raise ValueError('Nevalidni argumenti')
    else:
        svi_aerodromi[skracenica] = {
            'skracenica': skracenica,
            'pun_naziv': pun_naziv,
            'grad': grad,
            'drzava': drzava
        }
        return svi_aerodromi


"""
Funkcija koja čuva aerodrome u fajl.
"""


def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, 'w', newline='') as csvfile:
        aerodrom = ['skracenica', 'pun_naziv', 'grad', 'drzava']
        writer = csv.DictWriter(csvfile, fieldnames=aerodrom, delimiter=separator)
        writer.writeheader()
        for i in svi_aerodromi.keys():
            writer.writerow(svi_aerodromi[i])


"""
Funkcija koja učitava aerodrome iz fajla.
"""


def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    svi_aerodromi = {}
    with open(putanja, 'r', newline='') as csvfile:
        next(csvfile)
        row = csvfile.readline().split(separator)
        while not row[0] == '':
            svi_aerodromi[row[0]] = {
                'skracenica': row[0],
                'pun_naziv': row[1],
                'grad': row[2],
                'drzava': row[3][:-2]
            }
            row = csvfile.readline().split(separator)
    return svi_aerodromi
