import os.path
from datetime import datetime, timedelta
import pandas as pd
from pandas_ods_reader import read_ods
from tkinter import Tk
import json
from ahk import AHK
from time import sleep
from . import zpt_queries, biala_lista
from . import slowniki
import pdfkit
import mt940
import xml.etree.ElementTree as ET
import glob, keyring, shutil
from simpledbf import Dbf5
from django.contrib.staticfiles.storage import staticfiles_storage
from . import Kamsoft_Database, Maile

# FORMATY DAT #############################################
def data_today():
    data = datetime.now().strftime('%Y-%m-%d')
    return data

def data_today_with_time():
    data = datetime.now().strftime('%Y-%m-%d   -   %H:%M')
    return data

def data_miesiac_today():
    data = datetime.now().strftime('%Y-%m')
    return data

def data_miesiac_with_time():
    data = datetime.now().strftime('%Y-%m   -   %H:%M')
    return data

def alert_message(info='', alert='information', fade=True):
    if alert == 'information':
        bg_color = '#78c47a'
    elif alert == 'error':
        bg_color = 'red'
    elif alert == 'warning':
        bg_color = 'grey'

    if fade == True:
        id_alert = 'alert_message'
    else:
        id_alert = 'alert_message_no_fade'

    if info != '':
        text = f'<div class="container" id="{id_alert}"' \
               f' style="color: black; background-color: {bg_color}; font-size: 12px; ' \
               f'padding-top: 3px; padding-bottom: 3px; text-align: center;">' \
               f'{info}' \
               f'</div>'
        return text
    return info

# ONLINE #############################################
# formatowanie kwot
def currency_format(i):
    currency = str(round(i,2))
    if currency == '0':
        return currency

    if currency[-3] == '.':
        pass
    else:
        currency += '0'

    if len(currency) > 6:
        sep_number = int(len(currency) / 3) - 1
        m = 0
        for n in range(sep_number):
            currency = currency[:-(6 + (3 * n) + m)] + ' ' + currency[-(6 + (3 * n) + m):]
            m += 1
    return f'{currency}'

# FOOTER ##############################################
# pobieranie danych z tablicy aktualizacjia do i zwrócenie słownika do stopki strony
def footer_data():
    footer_data = {}
    footer_year = datetime.now().year
    footer_data['footer_year'] = footer_year
    query = f'SELECT apteka, data FROM aktualizacja order by apteka'
    dane = zpt_queries.zpt_query_fetchall(query)
    dane_dict = dict(dane)

    footer_data['dane'] = {}
    footer_data['alert'] = {}

    for n in range(2, 9):
        if n == 3:
            continue

        footer_data['alert'][n] = change_color_if_deley(dane_dict[n])
        footer_data['dane'][n] = str(dane_dict[n])[0:16]

    return footer_data

# sprawdzanie czasu, czy nie ma spóźnienia w aktualiacji
def change_color_if_deley(czas, spoznienie=300):
    czas_datetime = datetime.strptime(czas[0:19], "%Y-%m-%d %H:%M:%S")
    difference = (datetime.now() - czas_datetime).total_seconds()
    if difference > spoznienie:
        return '#c34f4f'
    return '#34730a'

# NAVBAR #############################################
# zwrot tablicy z opisem linku aktywnego w navbar
def active_link_navbar(link):

    active_link_list = []
    slownik = slowniki.linki_active
    for key in slownik:
        if slownik[key] == link:
            active_link_list.append('active')
        else:
            active_link_list.append('')
    return active_link_list

# GOTÓWKI #############################################
# saldo gotóki w kasie głównej
def get_saldo():
    query = f'SELECT SUM(kwota) FROM gotowki'
    wynik = zpt_queries.zpt_query_fetchone(query)[0]
    saldo_foramt = currency_format(float(wynik))

    saldo = f'<p style=" color: #c34f4f; text-align: center; font-size:14px;"><strong >' \
            f'SALDO: {saldo_foramt} zł</strong></p>'
    return saldo

def if_kwota_number(kwota):
    try:
        int(kwota)
    except ValueError:
        return False
    return True

def add_gotowki_to_zptdb(dane):
    if if_kwota_number(dane[2]):
        data_wybor = dane[0]
        apteka_wybor = int(dane[1])
        kwota = int(dane[2])
        opis = dane[3]
        query = f'INSERT INTO gotowki( data, id_apteka, kwota, opis)' \
                f' VALUES("{data_wybor}",{apteka_wybor},{kwota},"{opis}")'
        zpt_queries.zpt_query_modify(query)

def get_data_gotowki_edycja(id_gotowki):
    query = f'SELECT data, id_apteka, kwota, opis FROM gotowki WHERE id_got = {id_gotowki}'
    wynik = zpt_queries.zpt_query_fetchone(query)
    return wynik

def update_gotowki(dane):
    query = f'UPDATE gotowki SET data = "{dane[1]}", id_apteka = {dane[2]},' \
                            f'kwota = {dane[3]}, opis = "{dane[4]}" WHERE id_got = {dane[0]}'
    zpt_queries.zpt_query_modify(query)

def gotowki_delete(id_gotowki):
    query = f'DELETE FROM gotowki WHERE id_got = {id_gotowki}'
    zpt_queries.zpt_query_modify(query)

# KOSZTY #############################################
# lista_kontrahentow
def get_lista_kontrahentow_koszty():
    query = f'SELECT id_kont, nazwa FROM platnosci_kontrahenci ORDER BY nazwa ASC'
    lista = zpt_queries.zpt_query_fetchall(query)
    lista_empty_start= ((0, 'KONTRAHENT'),) + lista
    return lista_empty_start

#sprawdzenie czy kwota jest float
def if_kwota_float(kwota):
    try:
        float(kwota)
    except ValueError:
        return False
    return True

def add_koszty_to_zptdb(dane):
    if dane[2] != '' and if_kwota_float(dane[2]):
        query = f'INSERT INTO platnosci_fv( id_kont, nr_fv, kwota, data_platnosci, data_zaplaty, zaplacone)' \
                            f' VALUES({dane[0]},"{dane[1]}",{dane[2]},' \
                            f'"{dane[3]}", "", 0)'
        zpt_queries.zpt_query_modify(query)
        return True
    return  False

def get_data_koszty_edycja(id_koszty):
    query = f'SELECT id_kont, nr_fv, kwota, data_platnosci FROM platnosci_fv WHERE id_fv = {id_koszty}'
    wynik = zpt_queries.zpt_query_fetchone(query)
    return wynik

def get_koszty_suma():
    query = f'SELECT SUM(kwota) FROM ' \
             f'platnosci_fv WHERE ' \
             f'zaplacone = 0'
    wynik = zpt_queries.zpt_query_fetchone(query)[0]
    if wynik == None:
        return 0
    return round(wynik,2)

def get_faktury_towar_saldo():
    query = f'SELECT SUM(kwota) FROM platnosci_towar WHERE zaplacone = 0'
    wynik = zpt_queries.zpt_query_fetchone(query)[0]
    return round(wynik, 2)

def koszty_update(dane):
    print(dane)
    if dane[3] != '' and if_kwota_float(dane[3]):
        query = f'UPDATE platnosci_fv SET id_kont = {dane[1]}, nr_fv = "{dane[2]}",' \
                        f'kwota = {dane[3]}, data_platnosci = "{dane[4]}" WHERE id_fv = {int(dane[0])}'
        zpt_queries.zpt_query_modify(query)
        return True
    return False

def koszt_delete(id_koszt):
    query = f'DELETE FROM platnosci_fv WHERE id_fv = {id_koszt}'
    zpt_queries.zpt_query_modify(query)

def koszty_kontrahent_dodaj(dane):
    query = f'INSERT INTO platnosci_kontrahenci(nazwa, nip, konto) VALUES ("{dane[0]}","{dane[1]}","{dane[2]}")'
    zpt_queries.zpt_query_modify(query)

def get_dane_koszty_kontrahent_edycja(id_kontrahent):
    query = f'SELECT nazwa, nip, konto FROM platnosci_kontrahenci WHERE id_kont = {id_kontrahent}'
    wynik = zpt_queries.zpt_query_fetchone(query)
    return wynik

def koszty_kontrahent_update(dane):
    query = f'UPDATE platnosci_kontrahenci SET nazwa = "{dane[1]}", nip = "{dane[2]}",' \
                        f'konto = "{dane[3]}" WHERE id_kont = {dane[0]}'
    zpt_queries.zpt_query_modify(query)

def koszty_kontrahent_delete(id_kontrahenta):
    query = f'DELETE FROM platnosci_kontrahenci WHERE id_kont = {id_kontrahenta}'
    zpt_queries.zpt_query_modify(query)

def towar_dostawcy_dodaj(dane):
    query = f'INSERT INTO dostawcy(nazwa, nip, konto, id_02, id_03, id_04, id_05, id_06, id_07, id_08) VALUES' \
            f'("{dane[0]}", "{dane[1]}", "{dane[2]}", {dane[3]}, 0, {dane[4]}, {dane[5]}, {dane[6]}, {dane[7]}, {dane[8]})'
    zpt_queries.zpt_query_modify(query)

def get_dane_towar_dostawcy_edycja(id_dostawcy):
    query = f'SELECT nazwa, nip, konto, id_02, id_04, id_05, id_06, id_07, id_08 FROM ' \
            f'dostawcy WHERE id = {id_dostawcy}'
    wynik = zpt_queries.zpt_query_fetchone(query)
    return wynik

def towar_dostawcy_edytuj(dane):
    query = f'UPDATE dostawcy SET nazwa = "{dane[1]}", nip = "{dane[2]}",' \
            f'konto = "{dane[3]}", id_02 = "{dane[4]}", id_04 = "{dane[5]}",' \
            f' id_05 = "{dane[6]}", id_06 = "{dane[7]}", id_07 = "{dane[8]}",' \
            f' id_08 = "{dane[9]}"  WHERE id = {dane[0]}'
    zpt_queries.zpt_query_modify(query)

def towar_dostawcy_delete(id_dostawcy):
    query = f'DELETE FROM dostawcy WHERE id = {id_dostawcy}'
    zpt_queries.zpt_query_modify(query)

def get_dane_dodaj_towar_faktura_bufor(faktura):
    query = f'SELECT * FROM platnosci_towar WHERE nrfv = "{faktura}"'
    wynik = zpt_queries.zpt_query_fetchone(query)
    return wynik

def get_dane_dodaj_koszty_faktura_bufor(faktura):
    query = f'SELECT f.nr_fv, f.kwota, k.nazwa, k.nip, k.konto' \
            f' FROM platnosci_fv f, platnosci_kontrahenci k WHERE k.id_kont = f.id_kont and f.id_fv = "{faktura}"'
    wynik = zpt_queries.zpt_query_fetchone(query)
    return wynik

def get_konto_dostawcy(dostawca):
    query = f'SELECT konto, nip  FROM dostawcy WHERE id = {dostawca}'
    wynik = zpt_queries.zpt_query_fetchone(query)
    return wynik

def dodaj_towar_fakruty_do_bufora(lista_faktur):
    rodzaj = 'T'
    for faktura in lista_faktur:
        id_f = faktura
        dane = get_dane_dodaj_towar_faktura_bufor(faktura)
        kontrahent = dane[8]
        kwota = dane[5]
        tytul = faktura
        konto_nip = get_konto_dostawcy(dane[1])
        konto = konto_nip[0]
        nip = konto_nip[1]
        id_zestawienia = 0

        query = f'INSERT INTO przelewy_bankowe_bufor(rodzaj, id_f, kontrahent, konto_bankowe, kwota, data,' \
                f' tytul, nip, id_zestawienia) ' \
                f'VALUES("{rodzaj}", "{id_f}", "{kontrahent}", "{konto}", "{kwota}", "",' \
                f' "{tytul}", "{nip}", {id_zestawienia})'
        zpt_queries.zpt_query_modify(query)

def dodaj_koszty_fakruty_do_bufora(lista_faktur):
    rodzaj = 'K'
    for faktura in lista_faktur:
        id_f = faktura
        dane = get_dane_dodaj_koszty_faktura_bufor(faktura)
        kontrahent = dane[2]
        kwota = dane[1]
        tytul = dane[0]
        konto = dane[4]
        nip = dane[3]
        id_zestawienia = 0

        query = f'INSERT INTO przelewy_bankowe_bufor(rodzaj, id_f, kontrahent, konto_bankowe, kwota, data,' \
                f' tytul, nip, id_zestawienia) ' \
                f'VALUES("{rodzaj}", "{id_f}", "{kontrahent}", "{konto}", "{kwota}", "",' \
                f' "{tytul}", "{nip}", {id_zestawienia})'
        zpt_queries.zpt_query_modify(query)

def usun_towar_faktura_z_bufora(id_bufor, czynnosc = 'EKSP'):

    #rozróżnienie czy został naciśnięty 'kosz' czy eksport do pliku w buforze
    if czynnosc == 'DEL':
        #sprawdz czy pozycja w buforze dotyczy hurtowni
        query = f'SELECT id_zestawienia FROM przelewy_bankowe_bufor WHERE id_bufor = {id_bufor}'
        wynik = zpt_queries.zpt_query_fetchone(query)[0]


        if wynik != 0:
            #zapisanie danych spowrotem do hurtownie_do_zaplaty
            powrot_danych_do_hurtownie_do_zaplaty(wynik)

            # usuwanie zestawienia z hurtownie_zestawienia
            query = f'DELETE FROM hurtownie_zestawienia WHERE id_zestawienia = {wynik}'
            zpt_queries.zpt_query_modify(query)

    else:
        pass

    #usuwanie pozycji z bufora
    query = f'DELETE FROM przelewy_bankowe_bufor WHERE id_bufor = {id_bufor}'
    zpt_queries.zpt_query_modify(query)

def powrot_danych_do_hurtownie_do_zaplaty(id_zestawienia):
    query = f'SELECT hurtownia, json_dumb FROM hurtownie_zestawienia WHERE id_zestawienia = {id_zestawienia}'
    wynik = zpt_queries.zpt_query_fetchone(query)

    hurtownia = wynik[0]

    #pobranie danych z hurtownie_do_zaplaty dla danej hurtowni
    query_do_zaplaty = F'SELECT dane_json FROM hurtownie_do_zaplaty WHERE hurtownia = "{hurtownia}"'
    wynik_do_zaplaty = zpt_queries.zpt_query_fetchone(query_do_zaplaty)[0]

    #połączenie tablic + konwersja na string do zapisu
    suma_wynikow = str(json.loads(wynik[1]) + json.loads(wynik_do_zaplaty)).replace('\'','\"')

    #update danych w hurtownia_do_zaplaty
    query_update = f"UPDATE hurtownie_do_zaplaty SET dane_json = '{suma_wynikow}' WHERE hurtownia = '{hurtownia}'"
    zpt_queries.zpt_query_modify(query_update)

def eksport_przelwow_do_pliku():
    dane_bufor = get_dane_tabela_bufor()
    lista_przelewow = []

    for key in dane_bufor:
        #dane do zapisu do pliku
        linia_przelewu = generuj_linie_przelewu(dane_bufor[key])
        lista_przelewow.append(linia_przelewu)

        #biala lista
        nazwa = dane_bufor[key][0][3]
        konto = dane_bufor[key][0][4]
        nip = dane_bufor[key][0][8]
        biala_lista.zapisz_sprawdzenie_biala_lista(nazwa, konto, nip)

        #oznaczanie zapałaconych fv
        if dane_bufor[key][0][1] == 'T':
            towar_zaznacz_zapłacone(dane_bufor[key])

        elif dane_bufor[key][0][1] == 'K':
            koszty_zaznacz_zapłacone(dane_bufor[key])


        #zapis do tablicy przelewy
        zapis_do_tablicy_przelewy(dane_bufor[key], linia_przelewu)

        #usuwanie z tablicy przelewy_bankowe_bufor
        for d in dane_bufor[key]:
            usun_towar_faktura_z_bufora(d[0])


    n = 0
    plik_przelewu = fr"C:\Users\tomas\Dysk Google\ZPT_DATA\PRZELEWY\\{str(datetime.today().date()).replace('-', '')}_{n}.txt"
    while os.path.isfile(plik_przelewu):
        n += 1
        plik_przelewu = fr"C:\Users\tomas\Dysk Google\ZPT_DATA\PRZELEWY\\{str(datetime.today().date()).replace('-', '')}_{n}.txt"

    with open(plik_przelewu, 'w', encoding='utf-8') as f:
        for przelew in lista_przelewow:
            f.write(przelew)

def zapis_do_tablicy_przelewy(dane, linia_przelewu):
    tytul = ''
    kwota_przelewu = 0

    kontrahent = dane[0][3]
    zaplacone = 1
    id_zestawienia = dane[0][9]
    if dane[0][6] == '':
        data = data_today()
    else:
        data = dane[0][6]

    for d in dane:
        tytul += f'{d[7]}, '
        kwota_przelewu += float(d[5])

    tytul = f'({dane[0][1]}) ' + tytul[:-2]
    linia_przelewu_edit = linia_przelewu.replace('"', '""')
    kwota_przelewu = str(round(kwota_przelewu,2))
    query = f'INSERT INTO przelewy_bankowe(kontrahent, data, kwota, tytul, text_przelew, zaplacone, id_zestawienia) ' \
            f'VALUES("{kontrahent}", "{data}","{kwota_przelewu}", "{tytul}", "{linia_przelewu_edit}",' \
            f' {zaplacone}, {id_zestawienia})'
    zpt_queries.zpt_query_modify(query)

def towar_zaznacz_zapłacone(dane):
    for d in dane:
        id_fv = d[2]
        query = f'UPDATE platnosci_towar SET zaplacone = 1, data_zaplaty = "{data_today()}" WHERE nrfv = "{id_fv}"'
        zpt_queries.zpt_query_modify(query)

def koszty_zaznacz_zapłacone(dane):
    for d in dane:
        id_fv = d[2]
        query = f'UPDATE platnosci_fv SET zaplacone = 1, data_zaplaty = "{data_today()}" WHERE id_fv = {id_fv}'
        zpt_queries.zpt_query_modify(query)

def generuj_linie_przelewu(dane):
    kwota_przelewu = 0
    tytul_do_podzialu = ''
    rodzaj = ''
    identyfikator = ''

    for d in dane:
        if d[6] == '':
            data_zlecenia = str(datetime.today().date()).replace('-', '')
        else:
            data_zlecenia = d[6].replace('-', '')

        kwota_przelewu += float(d[5])
        rachunek_odbiorcy = f'"{d[4].replace(" ", "")}"'
        nazwa_adres_odbiorcy = f'"{podziel_tytul(d[3])}"'
        tytul_do_podzialu += f'{d[7]}, '
        rodzaj = d[1]

        if d[3] == 'ZUS':
            identyfikator = 'ZUS'
            kod_zlecenia = '120'
            nazwa_adres_odbiorcy = '"ZAKŁAD UBEZPIECZEŃ SPOŁECZNYCH"'
            tytul_zus = f'5472110371|R241297157|M{d[7].replace("/","")}01|'

        elif d[3] == 'US PIT4':
            identyfikator = 'PIT4'
            kod_zlecenia = '110'
            tytul_pit4 = f'/TI/N5472110371|/OKR/{d[7][2:4]}M{d[7][-2:]}|/SFP/PIT4'
            nazwa_adres_odbiorcy = '""'
        elif d[3] == 'US VAT':
            identyfikator = 'VAT'
            kod_zlecenia = '110'
            tytul_vat7 = f'/TI/N5472110371|/OKR/{d[7][2:4]}M{d[7][-2:]}|/SFP/VAT-7'
            nazwa_adres_odbiorcy = '""'
        elif d[3] == 'US CIT':
            identyfikator = 'CIT'
            kod_zlecenia = '110'
            tytul_cit = f'/TI/N5472110371|/OKR/{d[7][2:4]}M{d[7][-2:]}|/SFP/CIT'
            nazwa_adres_odbiorcy = '""'
        else:
            kod_zlecenia = '110'


    kwota_przelewu = f'{round(kwota_przelewu,2):0.2f}'.replace(',', '').replace('.', '')
    nr_rozliczeniowy_banku_zelceniodawcy = '11602202'
    pole_zerowe_pozycja_5 = '0'
    rachunek_zleceniodawcy = '"71116022020000000469095212"'
    adres_zleceniodawcy = '""'
    pole_zerowe_pozycja_10 = '0'
    nr_rozliczeniowy_banku_odbiorcy = ''
    pole_puste_pozycja_13 = '""'
    pole_puste_pozycja_14 = '""'
    kod_klasyfikacji = '"51"'
    adnotacje = '""'
    tytul_do_podzialu = podziel_tytul(f'({rodzaj}) ' + tytul_do_podzialu[:-2])

    if identyfikator == 'ZUS':
        tytul_do_podzialu = tytul_zus
    elif identyfikator == 'PIT4':
        tytul_do_podzialu = tytul_pit4
        kod_klasyfikacji = '"71"'
    elif identyfikator == 'VAT':
        tytul_do_podzialu = tytul_vat7
        kod_klasyfikacji = '"71"'
    elif identyfikator == 'CIT':
        tytul_do_podzialu = tytul_cit
        kod_klasyfikacji = '"71"'


    if podziel_tytul(tytul_do_podzialu) != False:
        linia_przelewu = f'{kod_zlecenia},{data_zlecenia},{kwota_przelewu},{nr_rozliczeniowy_banku_zelceniodawcy},' \
                         f'{pole_zerowe_pozycja_5},{rachunek_zleceniodawcy},{rachunek_odbiorcy},{adres_zleceniodawcy},' \
                         f'{nazwa_adres_odbiorcy},{pole_zerowe_pozycja_10},{nr_rozliczeniowy_banku_odbiorcy},' \
                         f'"{tytul_do_podzialu}",{pole_puste_pozycja_13},{pole_puste_pozycja_14},' \
                         f'{kod_klasyfikacji},' \
                         f'{adnotacje}\n'

    return linia_przelewu

def podziel_tytul(tytul):
    if tytul == '':
        return False
    if len(tytul) > 140:
        return False
    if len(tytul) > 105:
        tytul_podzielony = f'{tytul[0:35]}|{tytul[35:70]}|{tytul[70:105]}|{tytul[105:]}'
        return tytul_podzielony
    if len(tytul) > 70 and len(tytul) <= 105:
        tytul_podzielony = f'{tytul[0:35]}|{tytul[35:70]}|{tytul[70:]}'
        return tytul_podzielony
    if len(tytul) > 35 and len(tytul) <= 70:
        tytul_podzielony = f'{tytul[0:35]}|{tytul[35:]}'
        return tytul_podzielony
    if len(tytul) <= 35:
        tytul_podzielony = tytul
        return tytul_podzielony

def get_dane_tabela_bufor():
    query = f'SELECT * FROM przelewy_bankowe_bufor'
    wynik = zpt_queries.zpt_query_fetchall(query)

    wynik_dict = {}
    for n in wynik:
        if n[3] not in wynik_dict.keys():
            wynik_dict[f'{n[3]}'] = []
            wynik_dict[f'{n[3]}'].append(n)
        else:
            wynik_dict[f'{n[3]}'].append(n)
    return wynik_dict

def hurtownie_import_faktur(hurtownia, plik):
    if hurtownia == 'NOVO':
        dodaj_faktury_novo(hurtownia, plik)
    elif hurtownia == 'NEUCA':
        dodaj_faktury_neuca(hurtownia, plik)
    elif hurtownia == 'HURTAP':
        dodaj_faktury_hurtap(hurtownia, plik)
    elif hurtownia == 'PGF':
        dodaj_faktury_pgf(hurtownia, plik)
    elif hurtownia == 'FARMACOL':
        dodaj_faktury_farmacol(hurtownia, plik)
    elif hurtownia == 'ASTRA':
        dodaj_faktury_astra(hurtownia, plik)

def dodaj_faktury_novo(hurtownia, plik):
    nowe_dane = pd.read_excel(plik)
    nowe_dane.drop(['Skrót nazwy', 'Spóźn.', 'Data sprzedaży', 'Okres pł.', 'Zaliczka', 'Waluta'],
                   axis=1, inplace=True)
    puste_linie_filtr = nowe_dane[nowe_dane['Nr dokumentu'].isnull() != False].index
    nowe_dane.drop(puste_linie_filtr, inplace=True)
    nowe_dane_list = nowe_dane.values.tolist()
    nowe_dane_list.sort(key=lambda x: x[2])
    lista_koncowa = [[x[0], x[1], x[2], x[3], x[4].replace(' ',''), x[5].replace(' ','')] for x in nowe_dane_list]

    eksportuj_dane_do_zaplaty_do_bazy(lista_koncowa, hurtownia)

def dodaj_faktury_neuca(hurtownia, plik):
    nowe_dane = pd.read_excel(plik, skiprows=26, header=1)
    nowe_dane.drop(['Apteka', 'Indywidualny numer zamówienia', 'Typ', 'Po terminie', 'Data rozliczenia',
                    'Przedstawicielstwo'], axis=1, inplace=True)
    nowe_dane = nowe_dane[['Kod kontrahenta', 'Numer dokumentu', 'Termin zapłaty', 'Data wystawienia',
                           'Wartość brutto', 'Do zapłaty']]
    nowe_dane.rename(columns={'Kod kontrahenta': 'Nr kontr.',
                              'Numer dokumentu': 'Nr dokumentu',
                              'Termin zapłaty': 'Data płatności',
                              'Data wystawienia': 'Data wystawienia',
                              'Wartość brutto': 'Wartość brutto',
                              'Do zapłaty': 'Do zapłaty',
                              }, inplace=True)
    nowe_dane['Data wystawienia'].dt.strftime('%Y-%m-%d')
    nowe_dane['Data płatności'].dt.strftime('%Y-%m-%d')
    nowe_dane_list = nowe_dane.values.tolist()
    nowe_dane_list.sort(key=lambda x: x[2])
    nowe_dane_bez_timestamp = []
    for n in nowe_dane_list:
        nowe_dane_bez_timestamp.append([n[0], n[1], n[2].strftime('%Y-%m-%d'),
                                        n[3].strftime('%Y-%m-%d'), n[4], n[5]])

    eksportuj_dane_do_zaplaty_do_bazy(nowe_dane_bez_timestamp, hurtownia)

def dodaj_faktury_hurtap(hurtownia, plik):
    dane_z_pliku = []
    df = read_ods(plik, 'Sheet1')
    dane = df.values.tolist()
    for d in dane:
        print(len(str(d[6])))
        if len(str(d[7])[:-2]) == 5:
            dane_z_pliku.append([str(d[7])[:-2], d[1], str(d[3]), str(d[2]), d[6], d[6]])
        if len(str(d[6])[:-2]) == 5 and str(d[5]) != 'P':
            dane_z_pliku.append([str(d[6])[:-2], d[1], str(d[3]), str(d[2]), d[5], d[5]])

        if d[7] == 'ZŁ':
            if isinstance(d[6], str):
                kwota = round(float(str(d[6]).replace(' ', '').replace(',', '.')), 2)
            else:
                kwota = d[6]
            dane_z_pliku.append(['', d[1], str(d[3]), str(d[2]), kwota, kwota])

    dane_z_pliku.sort(key=lambda x: x[2])
    print(dane_z_pliku)
    eksportuj_dane_do_zaplaty_do_bazy(dane_z_pliku, hurtownia)

def dodaj_faktury_pgf(hurtownia, plik):
    df = pd.read_excel(plik, skiprows=10, skipfooter=5)
    dane_z_pliku = []
    dane = df.values.tolist()
    for d in dane:
        dane_z_pliku.append(['33114', d[0], d[2], d[1], d[3], d[5]])
    eksportuj_dane_do_zaplaty_do_bazy(dane_z_pliku, hurtownia)

def dodaj_faktury_astra(hurtownia, plik):
    df = pd.read_excel(plik, skiprows=6)
    dane_z_pliku = []

    dane = df.values.tolist()
    for d in dane:
        dane_z_pliku.append(['', str(d[1]), str(d[4])[:10], str(d[3])[:10], d[6], d[6]])
    eksportuj_dane_do_zaplaty_do_bazy(dane_z_pliku, hurtownia)

def dodaj_faktury_farmacol(hurtownia, plik):
    clipboard = Tk().clipboard_get()
    print(clipboard)
    dane_lista = []
    for n in clipboard.split('\n'):
        kwota = n.split(' ')[4].replace('.', '').replace(',','.')
        if kwota[-1] == '-':
            kwota = f'-{kwota[:-1]}'
        dane_lista.append(['39505', f"{n.split(' ')[1]}",
                           f"{n.split(' ')[3][-4:]}-{n.split(' ')[3][3:-5]}-{n.split(' ')[3][:2]}",
                           f"{n.split(' ')[2][-4:]}-{n.split(' ')[2][3:-5]}-{n.split(' ')[2][:2]}",
                           f"{kwota}",
                           f"{kwota}"])
    eksportuj_dane_do_zaplaty_do_bazy(dane_lista, hurtownia)

def eksportuj_dane_do_zaplaty_do_bazy(dane, hurtownia):

    dane_json = json.dumps(dane, ensure_ascii=False).encode('utf8').decode()

    query_del_old = f'DELETE FROM hurtownie_do_zaplaty WHERE hurtownia = "{hurtownia}"'
    zpt_queries.zpt_query_modify(query_del_old)

    query_insert = f"INSERT INTO hurtownie_do_zaplaty(hurtownia, dane_json) VALUES('{hurtownia}', '{dane_json}')"
    zpt_queries.zpt_query_modify(query_insert)

def eksportuj_do_hurtownie_zestawienia(hurtownia, dane, data):
    dane_tabela_zestawienie = []
    saldo = 0
    for d in dane:
        if d[2] <= data:
            saldo += float(d[4])
            dane_tabela_zestawienie.append(d)

    dane_ = str(dane_tabela_zestawienie).replace('\'','\"')
    query = f"INSERT INTO hurtownie_zestawienia(hurtownia, data, json_dumb) " \
            f"VALUES('{hurtownia}', '{datetime.today().date()}', '{dane_}')"
    zpt_queries.zpt_query_modify(query)

    # znajdz id zestawienia
    query_id = f'SELECT id_zestawienia FROM hurtownie_zestawienia ORDER BY id_zestawienia DESC LIMIT 1'
    wynik = zpt_queries.zpt_query_fetchone(query_id)

    usun_zaplacone_hurtownie_do_zaplaty(hurtownia, dane_)

    return wynik[0], f'{saldo:0.2f}'

def usun_zaplacone_hurtownie_do_zaplaty(hurtownia, dane):
    query = f'SELECT dane_json FROM hurtownie_do_zaplaty WHERE hurtownia = "{hurtownia}"'
    dane_calosc = zpt_queries.zpt_query_fetchone(query)[0]

    dane_pozostale = []
    for p in json.loads(dane_calosc):
        if p in json.loads(dane):
            pass
        else:
            dane_pozostale.append(p)

    if dane_pozostale == []:
        query_delete = f'DELETE FROM hurtownie_do_zaplaty WHERE hurtownia = "{hurtownia}"'
        zpt_queries.zpt_query_modify(query_delete)

    else:
        print('cos zostalo')
        dane_pozostale_ = str(dane_pozostale).replace('\'','\"')
        query_update = f"UPDATE hurtownie_do_zaplaty SET dane_json = '{dane_pozostale_}' WHERE hurtownia = '{hurtownia}'"
        zpt_queries.zpt_query_modify(query_update)

def dodaj_hurtownie_przelew_do_bufora(hurtownia, saldo, id_zestawienia):
    dane_hurtowni = slowniki.hurtownie_przelewy[hurtownia]

    query = f'INSERT INTO przelewy_bankowe_bufor(rodzaj, id_f, kontrahent, konto_bankowe,' \
            f' kwota, data, tytul, nip, id_zestawienia) VALUES(' \
            f'"H", "", "{dane_hurtowni["nazwa"]}", "{dane_hurtowni["konto"]}", "{saldo}", ' \
            f'"", "{dane_hurtowni["tytul"]}", "{dane_hurtowni["nip"]}", {id_zestawienia} )'
    zpt_queries.zpt_query_modify(query)

def oznacz_towar_faktury_gotowka(nr_faktury):
    query = f'UPDATE platnosci_towar SET zaplacone = 2, data_zaplaty = data_zak WHERE nrfv = "{nr_faktury}"'
    zpt_queries.zpt_query_modify(query)

def get_miesiac_hurtownie_poziom_zakupow():
    query = 'SELECT MAX(miesiac) FROM zakupy_hurtownie'
    wynik = zpt_queries.zpt_query_fetchone(query)

    return wynik

def zapisz_zmiany_pracownicy_dane(id_pracownika, dane):
    with open(staticfiles_storage.path('json/pracownicy.json'), "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        data[id_pracownika]["imie"] = dane['imie']
        data[id_pracownika]["nazwisko"] = dane['nazwisko']
        data[id_pracownika]["stanowisko"] = dane['stanowisko']
        data[id_pracownika]["badania"] = dane['badania']
        data[id_pracownika]["data_zakonczenia_umowy"] = dane['data_zakonczenia_umowy']
        if dane['aktywny'] == '0':
            data[id_pracownika]["aktywny"] = 'TAK'
        else:
            data[id_pracownika]["aktywny"] = 'NIE'
        data[id_pracownika]["placowka"] = dane['placowka']
        data[id_pracownika]["konto_bankowe"] = dane['konto_bankowe']
        data[id_pracownika]["pensja"] = dane['pensja']
        data[id_pracownika]["premia"] = dane['premia']
        data[id_pracownika]["pranie"] = dane['pranie']
        data[id_pracownika]["uwagi_wynagrodzenia"] = dane['uwagi_wynagrodzenia']
        data[id_pracownika]["data_urodzenia"] = dane['data_urodzenia']
        data[id_pracownika]["konto_bankowe"] = dane['konto_bankowe']

    with open(staticfiles_storage.path('json/pracownicy.json'), 'w') as outfile:
        json.dump(data, outfile)

def sprawdz_status_pracownika(id_pracownika):
    with open(staticfiles_storage.path('json/pracownicy.json'), "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    if data[id_pracownika]["aktywny"] == 'TAK':
        return True
    return False

def ustaw_kolumny_pracownicy_urlopy():
    rok = datetime.now().year
    lista_column = []
    for n in range(4):
        lista_column.append(rok - 3 + n)
    return lista_column

def pracownicy_nieobecnosci_dodaj(id_pracownika, rodzaj, data_od, data_do, uwagi):
    dane = get_dane_json_pracownika(id_pracownika)
    dane_json = json.loads(dane)
    dane_key = slowniki.rodzaje_niobecnosci_dane_json_keys[f'{rodzaj}']
    lista_dat = set_lista_dat_pracownicy_nieobecnosci_dodaj(data_od, data_do)

    if dane_key == 'urlopy':
        lata_urlopy_keys = dane_json[dane_key].keys()
        lista_dodane = []

        for date in lista_dat:
            if date[:4] not in lata_urlopy_keys:
                dane_json[dane_key][date[:4]] = []
            for key in lata_urlopy_keys:
                if len(dane_json[dane_key][key]) == 26 or date in lista_dodane:
                    continue
                else:
                    print(date)
                    dane_json[dane_key][key].append(date)
                    lista_dodane.append(date)

    else:
        for d in lista_dat:
            dane_json[dane_key].append([d, uwagi])

    dane_do_zapisu = json.dumps(dane_json)

    zapisz_pracownicy_nieobecnosci_do_bazy(id_pracownika, dane_do_zapisu)

def get_dane_json_pracownika(id_pracownika):
    query = f'SELECT dane_json FROM pracownicy_nieobecnosci WHERE id_pracownika = {id_pracownika}'
    wynik = zpt_queries.zpt_query_fetchone(query)[0]
    return wynik

def set_lista_dat_pracownicy_nieobecnosci_dodaj(data_od, data_do):
    lista_dat = []
    data_od_datetime = datetime.strptime(data_od, '%Y-%m-%d').date()
    data_do_datetime = datetime.strptime(data_do, '%Y-%m-%d').date()

    data_pomiedzy = data_od_datetime
    while True:
        if data_pomiedzy > data_do_datetime:
            break
        lista_dat.append(str(data_pomiedzy))
        data_pomiedzy += timedelta(days=1)
    return lista_dat

def zapisz_pracownicy_nieobecnosci_do_bazy(id_pracownika, dane_do_zapisu):
    query = f"UPDATE pracownicy_nieobecnosci SET dane_json = '{dane_do_zapisu}' WHERE id_pracownika = {id_pracownika}"
    zpt_queries.zpt_query_modify(query)

def usun_ostatni_wpis_pracownicy_nieobecnosci(id_pracownika, rodzaj):

    dane = get_dane_json_pracownika(id_pracownika)
    dane_json = json.loads(dane)
    dane_key = slowniki.rodzaje_niobecnosci_dane_json_keys[f'{rodzaj}']
    if rodzaj != '1':
        dane_json[dane_key].pop(-1)

    else:
        lata_urlopy_keys = []
        for key in dane_json[dane_key].keys():
            lata_urlopy_keys.append(key)
        lata_urlopy_keys.sort()
        lata_urlopy_keys.reverse()

        for rok in lata_urlopy_keys:
            if len(dane_json[dane_key][f'{rok}']) != 0:
                dane_json[dane_key][f'{rok}'].pop(-1)
                break

    dane_do_zapisu = json.dumps(dane_json)
    zapisz_pracownicy_nieobecnosci_do_bazy(id_pracownika, dane_do_zapisu)

def get_pracownicy_dane_wyplata():
    with open(staticfiles_storage.path('json/pracownicy.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    pracownicy_dane_wyplata = []
    for key in dane:
        if key != '23':
            urlopy = get_ilosc_urlopu_miesiac(f'{key}')
        else:
            urlopy = 0

        if dane[key]['aktywny'] == 'TAK':
            pracownicy_dane_wyplata.append({'id_pracownika': f'{key}',
                                            'pelna_nazwa': dane[key]['pelna_nazwa'],
                                            'pensja': dane[key]['pensja'],
                                            'uwagi': dane[key]['uwagi_wynagrodzenia'],
                                            'urlop': urlopy,
                                            'premia': dane[key]['premia'],
                                            'pranie': dane[key]['pranie']})
        else:
            continue

    pracownicy_dane_wyplata.sort(key=lambda x: x['pelna_nazwa'])

    return pracownicy_dane_wyplata

def get_ilosc_urlopu(id_pracownika):

    query = f'SELECT dane_json FROM pracownicy_nieobecnosci WHERE id_pracownika = {id_pracownika}'
    wynik = zpt_queries.zpt_query_fetchone(query)
    dane_json = json.loads(wynik[0])
    dane_urlopy = dane_json['urlopy']
    ilosc_urlopu = 0

    for key in dane_urlopy:
        urlop_rok = 26 - len(dane_urlopy[key])
        ilosc_urlopu += urlop_rok

    return ilosc_urlopu

def get_ilosc_urlopu_miesiac(id_pracownika):
    if id_pracownika == 25:
        return 0
    okres = str(datetime.now())[:7]
    query = f'SELECT dane_json FROM pracownicy_nieobecnosci WHERE id_pracownika = {id_pracownika}'
    wynik = zpt_queries.zpt_query_fetchone(query)
    dane_json = json.loads(wynik[0])
    dane_urlopy = dane_json['urlopy']
    urlopy_miesiac = 0

    for key in dane_urlopy:
        for d in dane_urlopy[key]:
            if okres in d:
                urlopy_miesiac += 1

    return urlopy_miesiac

def eksportuj_wynagrodzenia_do_pdf(dane, okres):
    config = pdfkit.configuration(wkhtmltopdf='c:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    file_html = staticfiles_storage.path('szablony/wzor_wyplaty.html')
    with open(file_html, "r", encoding='utf-8') as f:
        text = f.read()
    text = text.replace('miesiac_wynagrodzen', okres)
    text = text.replace('pola_z_wynagrodzeniami_pracownicy', set_wynagrodzenia_html_text(dane))

    plik_wyjsciowy = rf'C:\Users\tomas\Desktop\WYNAGRODZENIA_{okres}.pdf'
    pdfkit.from_string(text, plik_wyjsciowy, configuration=config)

    return True

def set_wynagrodzenia_html_text(dane):
    text_do_dodania = ''
    n = 1
    for d in dane:
        premia = d["premia"]
        pranie = d["pranie"]
        style_premia = ''
        style_pranie = ''

        if premia != '0,00':
            style_premia = 'style =" background:#cfcdc8"'
        else:
            style_premia = ''

        if pranie != '0,00':
            style_pranie = 'style =" background:#cfcdc8"'
        else:
            style_pranie = ''
        if d["nazwa"] == 'Zioła STEFAN':
            continue
        text_do_dodania += f'<tr> ' \
                           f'<td style="width: 5%">{n}</td>' \
                           f'<td >{d["nazwa"]}</td>' \
                           f'<td >{d["pensja"]} zł</td>' \
                           f'<td >{d["uwagi"]}</td>' \
                           f'<td >{d["urlopy"]}</td>' \
                           f'<td {style_premia}>{d["premia"]} zł</td>' \
                           f'<td {style_pranie}>{d["pranie"]} zł</td>' \
                           f'</tr>'
        n += 1

    text_do_dodania += f'<tr><td colspan="7"></td><p></p> </tr>'
    text_do_dodania += f'<tr> ' \
                       f'<td style="widtd: 5%">{n}</td>' \
                       f'<td >STEFAN ZIOŁA</td>' \
                       f'<td colspan="5">PREZES ZARZĄDU - ZLECENIE</td>' \
                       f'</tr>'

    return text_do_dodania

def get_pracownicy_wyplata_ostatni_przelew():
    with open(staticfiles_storage.path('json/pracownicy.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    pracownicy_dane_wyplata = []
    for key in dane:
        if dane[key]['aktywny'] == 'TAK':
            pracownicy_dane_wyplata.append({'id_pracownika': f'{key}',
                                            'pelna_nazwa': dane[key]['pelna_nazwa'],
                                            'ostatnia_wyplata': dane[key]['ostatnia_wyplata'],
                                            'konto_bankowe': dane[key]['konto_bankowe']})
        else:
            continue

    pracownicy_dane_wyplata.sort(key=lambda x: x['pelna_nazwa'])
    return pracownicy_dane_wyplata

def update_pracownicy_wyplata_ostatni_przelew(dane_do_przelewow):
    with open(staticfiles_storage.path('json/pracownicy.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    for d in dane_do_przelewow:
        dane[d['id_pracownika']]['ostatnia_wyplata'] = d['wyplata']

    with open(staticfiles_storage.path('json/pracownicy.json'), 'w') as outfile:
        json.dump(dane, outfile)

def generuj_dane_do_pracownicy_przelewy_bank(dane_do_przelewow):
    dzien_przelewu = get_ostatni_dzien_miesiaca_do_wyplaty()
    lista_przelewow = []
    for pracownik in dane_do_przelewow:
        wyplata = pracownik['wyplata'].replace(',','.')
        if wyplata == 'gotówka':
            continue
        else:
            pelna_nazwa = pracownik['pelna_nazwa']
            konto_bankowe = pracownik['konto_bankowe']

            if pelna_nazwa == 'Zioła STEFAN':
                tytul = f'UMOWA ZLECENIE {dzien_przelewu[:-3]}'
            else:
                tytul = f'WYNAGRODZENIE {dzien_przelewu[:-3]}'

            if wyplata == 'gotówka':
                continue
        linia_przelewu = generuj_linie_przelewu_wyplaty(pelna_nazwa, konto_bankowe, wyplata, dzien_przelewu, tytul)
        lista_przelewow.append(linia_przelewu)
        get_zapisz_przelew_wyplaty_do_bazy(pelna_nazwa, wyplata, linia_przelewu, tytul, dzien_przelewu)

    plik_przelewu = rf"G:\Mój dysk\ZPT_DATA\PRZELEWY\{dzien_przelewu.replace('-','')}_W.txt"
    # plik_przelewu = rf"C:\Users\tomas\Dysk Google\ZPT_DATA\PRZELEWY\{dzien_przelewu.replace('-','')}_W.txt"
    with open(plik_przelewu, 'w', encoding='utf-8') as f:
        for przelew in lista_przelewow:
            f.write(przelew)

def get_zapisz_przelew_wyplaty_do_bazy(pelna_nazwa, wyplata, linia_przelewu, tytul,  data):
    query = f"INSERT INTO przelewy_bankowe(kontrahent, data, kwota, tytul, text_przelew, zaplacone, id_zestawienia) " \
            f"VALUES('{pelna_nazwa}','{data}', '{wyplata}', '{tytul}', '{linia_przelewu}', 1, 0)"
    zpt_queries.zpt_query_modify(query)

def get_ostatni_dzien_miesiaca_do_wyplaty():
    # data ostatni dzien miesiaca
    offset = pd.tseries.offsets.BMonthEnd()
    data = datetime.now().date()
    data_ostatni = offset.rollforward(data).date()

    return str(data_ostatni)

def generuj_linie_przelewu_wyplaty(pelna_nazwa, konto_bankowe, wyplata, dzien_przelewu, tytul):
    kod_zlecenia = '110'
    data_zlecenia = dzien_przelewu.replace('-', '')
    kwota_przelewu = wyplata.replace(',', '').replace('.', '')
    nr_rozliczeniowy_banku_zelceniodawcy = '11602202'
    pole_zerowe_pozycja_5 = '0'
    rachunek_zleceniodawcy = '"71116022020000000469095212"'
    rachunek_odbiorcy = konto_bankowe.replace(' ','')
    adres_zleceniodawcy = '""'
    nazwa_adres_odbiorcy = pelna_nazwa
    pole_zerowe_pozycja_10 = '0'
    nr_rozliczeniowy_banku_odbiorcy = ''
    pole_puste_pozycja_13 = '""'
    pole_puste_pozycja_14 = '""'
    kod_klasyfikacji = '"51"'
    adnotacje = '""'
    tytul_do_podzialu = tytul

    linia_przelewu = f'{kod_zlecenia},{data_zlecenia},{kwota_przelewu},{nr_rozliczeniowy_banku_zelceniodawcy},' \
                     f'{pole_zerowe_pozycja_5},{rachunek_zleceniodawcy},"{rachunek_odbiorcy}",{adres_zleceniodawcy},' \
                     f'"{nazwa_adres_odbiorcy}",{pole_zerowe_pozycja_10},{nr_rozliczeniowy_banku_odbiorcy},' \
                     f'"{tytul_do_podzialu}",{pole_puste_pozycja_13},{pole_puste_pozycja_14},{kod_klasyfikacji},' \
                     f'{adnotacje}\n'

    return linia_przelewu

def fundusze_l_dodaj(data, kwota, opis):
    query = f'INSERT INTO gotowki_xx(data, opis, kwota) VALUES("{data}", "{opis}", "{kwota}")'
    zpt_queries.zpt_query_modify(query)

def fundusze_l_delete(id_poz):
    query = f'DELETE FROM gotowki_xx WHERE id = {id_poz}'
    zpt_queries.zpt_query_modify(query)

def get_dane_fundusze_l_edycja(id_edycja):
    query = f'SELECT * FROM gotowki_xx WHERE id = {id_edycja}'
    wynik = zpt_queries.zpt_query_fetchone(query)
    return wynik

def fundusze_l_update(data, kwota, opis, id_edycja):

    query = f'UPDATE gotowki_xx SET data = "{data}", kwota = "{kwota}", opis = "{opis}" WHERE id = {id_edycja}'
    zpt_queries.zpt_query_modify(query)

def fundusze_l_get_saldo():
    query = f'SELECT SUM(kwota) FROM gotowki_xx'
    wynik = zpt_queries.zpt_query_fetchone(query)[0]
    saldo_foramt = currency_format(float(wynik))

    saldo = f'<p style=" color: #c34f4f; text-align: center; font-size:14px;"><strong >' \
            f'SALDO: {saldo_foramt} zł</strong></p>'
    return saldo

def karty_hallera_uzupelnij_daty():
    with open(staticfiles_storage.path('json/karty_hallera.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    ostatnia_data = sorted(list(dane.keys()))[-1]
    data_now = datetime.now().date()

    lista_dat = pd.date_range(ostatnia_data, data_now,freq='d').tolist()[1:-1]
    lista_dat_str = []
    for d in lista_dat:
        lista_dat_str.append(str(d.date()))

    if lista_dat_str != []:
        for d in lista_dat_str:
            if d not in dane.keys():
                dane[d] = {}
            else:
                continue
            dane[d]['kwota_kamsoft'] = 0
            dane[d]['kwota_terminal'] = 0
            dane[d]['rozliczone'] = 0

    with open(staticfiles_storage.path('json/karty_hallera.json'), 'w') as outfile:
        json.dump(dane, outfile)

def karty_hallera_uzupelnij_dane_z_kamsoft():
    ks = Kamsoft_Database.DataBaseKamsoft()
    with open(staticfiles_storage.path('json/karty_hallera.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    for key in dane.keys():
        if dane[key]['kwota_kamsoft'] == 0 or dane[key]['rozliczone'] == 0:
            query = f"SELECT SUM(kwota) FROM dokp WHERE (iddedp = 2 OR iddedp = 17 ) " \
                    f"AND id_osu = 0 AND datsp='{key}'"
            wynik = ks.mysql_querry(query)
            if wynik[0][0] != None:
                kwota_kmsoft = round(float(wynik[0][0]), 2) * (-1)
            else:
                kwota_kmsoft = 0
            dane[key]['kwota_kamsoft'] = kwota_kmsoft
            if kwota_kmsoft == dane[key]['kwota_terminal']:
                dane[key]['rozliczone'] = 1
        else:
            pass

    with open(staticfiles_storage.path('json/karty_hallera.json'), 'w') as outfile:
        json.dump(dane, outfile)

    return dane

def karty_hallera_dodaj(data, kwota):
    with open(staticfiles_storage.path('json/karty_hallera.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    if data not in dane.keys():
        return False
    else:
        if kwota == '0':
            dane[data]['kwota_terminal'] = 0
        else:
            dane[data]['kwota_terminal'] = round(float(kwota.replace(',','.')),2)

    with open(staticfiles_storage.path('json/karty_hallera.json'), 'w') as outfile:
        json.dump(dane, outfile)
    return True

def karty_hallera_znajdz_braki(data, roznica):
    ks = Kamsoft_Database.DataBaseKamsoft()
    query_sumy_pacjenci = f"SELECT  nrkln, ROUND(SUM(zplcl),2) from sprz  where id>0 and" \
                          f" nrpar>0 and bufor=0 and wskus=0 and zplcl > 0 and datsp = '{data}'" \
                          f" AND iddokf = 0 AND idpaca = 0 GROUP BY nrkln ORDER BY SUM(zplcl) DESC "
    wynik_sumy = ks.mysql_querry(query_sumy_pacjenci)

    query_klienci_karta = f"SELECT nrkln FROM dokp WHERE (iddedp = 2 OR iddedp = 17 )" \
                          f" AND id_osu = 0 AND datsp='{data}'"
    wynik_pacjenci_karta = ks.mysql_querry(query_klienci_karta)
    lista_pacjenci_karta = []

    dane_zwrotne = ''
    for w in wynik_pacjenci_karta:
        lista_pacjenci_karta.append(w[0])
    suma_dzien = 0
    for n in wynik_sumy:
        if n[0] not in lista_pacjenci_karta:
            suma_dzien += n[1]
            if suma_dzien >= roznica:
                ostatnia_faktura_kwota = round(n[1] - (suma_dzien - roznica), 2)
                dane_zwrotne += f'P.{n[0]} - {ostatnia_faktura_kwota}'
                break
            else:
                dane_zwrotne += f'P.{n[0]} - {n[1]}; '
    return dane_zwrotne

def get_nowy_rachunek_nr():
    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    lista_int = []
    for key in dane:
        lista_int.append(int(key))

    ostatni_nr = dane[f'{max(lista_int)}']['nr']
    nr_kolejny = int(ostatni_nr[:ostatni_nr.index('/')]) + 1

    nowy_rachunek_nr = str(nr_kolejny) + f'/{str(datetime.now().date().year)}'
    return nowy_rachunek_nr

def get_kontrahent_key(id_rachunek):
    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    dane_kontrahenta = slowniki.czynsze_kontrahenci_dict
    nazwa = dane[id_rachunek]['najemca']
    for key in dane_kontrahenta:
        if dane_kontrahenta[key]['nazwa'] == nazwa:
            return key
        else:
            pass

def get_dane_rachunek(id_rachunek):
    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    return dane[id_rachunek]

def get_nowy_rachunek_key():
    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    lista_int = []
    for key in dane:
        lista_int.append(int(key))
    return max(lista_int) + 1

def oznaczenie_mail(rachunek_key):
    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    mail = dane[rachunek_key]['mail']
    return mail

def zapisz_zmiany_w_pliku_czynsze(key, dane_dict):
    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    dane[key] = dane_dict

    with open(staticfiles_storage.path('json/czynsze.json'), 'w') as outfile:
        json.dump(dane, outfile)

def eksportuj_rachunek_czynsz_pdf(id_rachunek):
    config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    file_html = staticfiles_storage.path('szablony/wzor_rachunek_czynsze.html')
    with open(file_html, "r", encoding='utf-8') as f:
        text = f.read()

    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    data_rachunku = dane[id_rachunek]['data']
    najemca = dane[id_rachunek]['najemca']
    if najemca in ['PIELGRZYMOWICE', 'HALLERA']:
        wystawca = 'MARIA KAPPEL-ZIOŁA'
    else:
        wystawca = 'MARIA KAPPEL-ZIOŁA'
    nr_rachunku = dane[id_rachunek]['nr']
    opis_1 = dane[id_rachunek]['pole_1']
    opis_2 = dane[id_rachunek]['pole_2']
    opis_3 = dane[id_rachunek]['pole_3']
    opis_4 = dane[id_rachunek]['pole_4']
    opis_5 = dane[id_rachunek]['pole_5']
    if dane[id_rachunek]['kwota_1'] != 0:
        kwota_1 = float(dane[id_rachunek]['kwota_1'])
    else:
        kwota_1 = ''
    if dane[id_rachunek]['kwota_2'] != 0:
        kwota_2 = float(dane[id_rachunek]['kwota_2'])
    else:
        kwota_2 = 0
    if dane[id_rachunek]['kwota_3'] != 0:
        kwota_3 = float(dane[id_rachunek]['kwota_3'])
    else:
        kwota_3 = 0
    if dane[id_rachunek]['kwota_4'] != 0:
        kwota_4 = float(dane[id_rachunek]['kwota_4'])
    else:
        kwota_4 = 0
    if dane[id_rachunek]['kwota_5'] != 0:
        kwota_5 = float(dane[id_rachunek]['kwota_5'])
    else:
        kwota_5 = 0

    suma_rachunku = dane[id_rachunek]['suma']
    licznik = dane[id_rachunek]['licznik']

    text = text.replace('data_wystawienia_rachunku', f'{data_rachunku}')
    najemca_dane = get_najemca_dane_adresowe(najemca)
    text = text.replace('wystawca_rachunku', f'{wystawca}')
    text = text.replace('nazwa_odbiorcy_rachunku', f'{najemca_dane[0]}')
    text = text.replace('adres_odbiorcy_rachunku', f'{najemca_dane[1]}')
    text = text.replace('nip_odbiorcy_rachunku', f'{najemca_dane[2]}')
    text = text.replace('numer_rachunku', f'{nr_rachunku}')
    text = text.replace('opis_1', f'{opis_1}')
    text = text.replace('opis_2', f'{opis_2}')
    text = text.replace('opis_3', f'{opis_3}')
    text = text.replace('opis_4', f'{opis_4}')
    text = text.replace('opis_5', f'{opis_5}')
    if kwota_1 != 0:
        text = text.replace('kwota_1', f'{kwota_1:.2f} zł')
    else:
        text = text.replace('kwota_1', f'')
    if kwota_2 != 0:
        text = text.replace('kwota_2', f'{kwota_2:.2f} zł')
    else:
        text = text.replace('kwota_2', f'')
    if kwota_3 != 0:
        text = text.replace('kwota_3', f'{kwota_3:.2f} zł')
    else:
        text = text.replace('kwota_3', f'')
    if kwota_4 != 0:
        text = text.replace('kwota_4', f'{kwota_4:.2f} zł')
    else:
        text = text.replace('kwota_4', f'')
    if kwota_5 != 0:
        text = text.replace('kwota_5', f'{kwota_5:.2f} zł')
    else:
        text = text.replace('kwota_5', f'')

    text = text.replace('suma_rachunku', f'{suma_rachunku:.2f} zł')

    nazwa_pliku = f'{nr_rachunku.replace("/", "_")}_{data_rachunku.replace("-", "")}_{najemca}_{suma_rachunku:.2f}'
    # plik_wyjsciowy = rf'C:\Users\tomas\Dysk Google\ZPT_DATA\Czynsze\{nazwa_pliku}.pdf'
    plik_wyjsciowy = rf'G:\Mój dysk\ZPT_DATA\CZYNSZE\{nazwa_pliku}.pdf'
    pdfkit.from_string(text, plik_wyjsciowy, configuration=config)

def get_najemca_dane_adresowe(najemca):
    slownik_najemcy = slowniki.czynsze_kontrahenci_dict
    for key in slownik_najemcy:
        if slownik_najemcy[key]['nazwa'] == najemca:
            dane_adresowe = [slownik_najemcy[key]['pole_adresowe_1'],
                             slownik_najemcy[key]['pole_adresowe_2'],
                             slownik_najemcy[key]['pole_adresowe_3'],
                             slownik_najemcy[key]['email']]
            return dane_adresowe
        else:
            continue
    return ['','','']

def czynsze_wyslij_mailem(id_rachunku):
    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    dane_rachunek = dane[id_rachunku]
    najemca = dane_rachunek['najemca']
    nr_rachunku = dane_rachunek['nr'].replace('/','_')
    kwota = str(dane_rachunek['suma'])
    miesiac_rachunku = dane_rachunek['data'][0:-3]
    mail_odbiorca = get_najemca_dane_adresowe(najemca)[3]

    # znajdz plik z rachunkiem
    lista_plikow = glob.glob(rf'C:\Users\tomas\Dysk Google\ZPT_DATA\CZYNSZE\*.pdf')
    plik_rachunek = ''
    for f in lista_plikow:
        if nr_rachunku in f and kwota in f:
            plik_rachunek = f
            break

    # zapytaj o hasło
    password = keyring.get_password("mejek_mail", "mejek_mail")

    # tekst wiadomości
    tutul_wiadomosci = f'Rachunek Pielgrzymowice {miesiac_rachunku}'
    text_wiadomosci = 'Pozdrawiam'

    mail = Maile.Maile()
    mail.mail_text_attachmen(mail_odbiorca, tutul_wiadomosci, text_wiadomosci, plik_rachunek,
                                                  password)

    return [nr_rachunku, mail_odbiorca]

def zmien_oznaczenie_mail(id_rachunek):
    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    dane[id_rachunek]['mail'] = 1

    with open(staticfiles_storage.path('json/czynsze.json'), 'w') as outfile:
        json.dump(dane, outfile)

def get_lista_dat_dyzury(data_start, data_stop):
    data_1 = datetime.strptime(data_start, '%Y-%m-%d')
    data_2 = datetime.strptime(data_stop, '%Y-%m-%d')
    date_modified = data_1
    lista_dat = [str(data_1.date())]

    while date_modified < data_2:
        date_modified += timedelta(days=1)
        lista_dat.append(str(date_modified.date()))
    return lista_dat

def dyzury_generuj_pdf(lista_dat):
    config = pdfkit.configuration(wkhtmltopdf='c:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    with open(staticfiles_storage.path('json/dyzury.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    text_do_dodania = ''

    for d in lista_dat:
        apteka = dane[d]['apteka']
        adres_1 = dane[d]['adres_1']
        adres_2 = dane[d]['adres_2']
        telefon = dane[d]['telefon']

        text_do_dodania += f'<tr>' \
                           f'<td style = "width: 15%"><b>{d}</b></td>' \
                           f'<td style = "width: 30%"><b>{apteka}</b></td>' \
                           f'<td style = "width: 35%"><b>{adres_1}</br>{adres_2}</b></td>' \
                           f'<td style = "width: 20%"><b>{telefon}</b></td>' \
                           f'</tr>'

    with open(staticfiles_storage.path('szablony/wzor_dyzury.html'), "r", encoding='utf-8') as f:
        text = f.read()
    text = text.replace('wiersze_do_dodania', text_do_dodania)

    pdfkit.from_string(text, fr'C:\Users\tomas\Desktop\DYZURY.pdf', configuration=config)

def dyzury_wyslij_emailem(data_start, data_stop):
    if os.path.isfile(r'C:\Users\tomas\Desktop\DYZURY.pdf'):
        mail = Maile.Maile()
        tutul_wiadomosci = f'DYŻURY {data_start} - {data_stop}'
        text_wiadomosci = 'Pozdrawiam'
        attachment = r'C:\Users\tomas\Desktop\DYZURY.pdf'
        password = keyring.get_password("mejek_mail", "mejek_mail")

        for mail_odbiorca in slowniki.dyzury_maile_apteki:
            pass
            mail.mail_text_attachmen(mail_odbiorca, tutul_wiadomosci, text_wiadomosci, attachment,
                                     password)
        return True
    else:
        return False

def get_lista_fv_do_rozliczenia(id_zestawienia):
    query = f'SELECT json_dumb FROM hurtownie_zestawienia WHERE id_zestawienia = {id_zestawienia}'
    wynik = zpt_queries.zpt_query_fetchone(query)[0]

    lista_faktur = []
    for d in json.loads(wynik):
        lista_faktur.append(str(d[1]))
    return lista_faktur

def rozlicz_przelew(id_zestawienia):
    ahk = AHK()
    faktury_do_rozliczenia = []
    zestawienie_lista = get_lista_fv_do_rozliczenia(id_zestawienia)
    zestawienie_test = zestawienie_lista
    test = 1
    sleep_time = 2

    lista_okien = list(ahk.windows())

    for okno in lista_okien:
        if 'Symfonia Finanse' in str(okno.title):
            okno.activate()
            sleep(1)
            break

        # else:
        #     print(lista_okien)
        #     print('nie działa')
        #     return 0

    ahk.mouse_move(1036, 124)
    ahk.right_click()
    sleep(1)
    ahk.mouse_move(1046, 131)
    ahk.click()
    sleep(sleep_time)
    data = Tk().clipboard_get().split('\n')
    for d in data:
        if d != '':
            d_split = d.split('\t')
            faktury_do_rozliczenia.append(d_split[6])
            # print(d_split[6], d_split[2])

    indeks_count = 0
    print(len(faktury_do_rozliczenia))
    indeksy = []

    for faktura_zestawienie in faktury_do_rozliczenia:

        if faktura_zestawienie in zestawienie_test:
            zestawienie_test.remove(f'{faktura_zestawienie}')
            indeksy.append(faktury_do_rozliczenia.index(f'{faktura_zestawienie}'))

    print(indeksy)
    print('OK')

    count = 0
    count_pgdn = 0
    number_of_pgdn = int(len(faktury_do_rozliczenia) / 41) + 1

    print(number_of_pgdn)
    for press_pgdn in range(0, number_of_pgdn):
        indeks_start = press_pgdn * 41
        indeks_stop = indeks_start + 41

        while int(indeksy[indeks_count]) >= indeks_start and int(indeksy[indeks_count]) < indeks_stop:
            pozycja_strona_y = ((int(indeksy[indeks_count]) % 41) * 17) + 130
            ahk.mouse_move(315, pozycja_strona_y)
            sleep(0.2)
            ahk.click(315, pozycja_strona_y)
            sleep(0.3)
            ahk.send('!r')
            sleep(0.3)
            print(indeks_count, indeks_start, indeks_stop, faktury_do_rozliczenia[int(indeksy[indeks_count])])
            # alt r
            if indeks_count == len(indeksy) - 1:
                break
            indeks_count += 1
        ahk.key_press('PgDn')
    print(f'ZOSTAŁO: {zestawienie_lista}')

def rozne_todo_zakoncz_zadanie(todo_task_id):
    with open(staticfiles_storage.path('json/todo.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    dane[f'{todo_task_id}']['status'] = '1'
    dane[f'{todo_task_id}']['data_zamkniecia'] = str(datetime.today().date())

    with open(staticfiles_storage.path('json/todo.json'), 'w') as outfile:
        json.dump(dane, outfile)

def rozne_todo_undone_zadanie(todo_task_id):
    with open(staticfiles_storage.path('json/todo.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    dane[f'{todo_task_id}']['status'] = '0'
    dane[f'{todo_task_id}']['data_zamkniecia'] = ''

    with open(staticfiles_storage.path('json/todo.json'), 'w') as outfile:
        json.dump(dane, outfile)

def get_dane_todo_task(todo_task_id):
    with open(staticfiles_storage.path('json/todo.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    return dane[todo_task_id]

def update_todo_task(todo_task_id, nazwa, opis, data_dodania, termin):
    with open(staticfiles_storage.path('json/todo.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    if todo_task_id not in dane.keys():
        dane[todo_task_id] = {}
        dane[todo_task_id]['nazwa'] = ''
        dane[todo_task_id]['opis'] = ''
        dane[todo_task_id]['data_dodania'] = ''
        dane[todo_task_id]['termin'] = ''
        dane[todo_task_id]['data_zamkniecia'] = ''
        dane[todo_task_id]['status'] = '0'

    dane[todo_task_id]['nazwa'] = nazwa
    dane[todo_task_id]['opis'] = opis
    dane[todo_task_id]['data_dodania'] = data_dodania
    dane[todo_task_id]['termin'] = termin

    with open(staticfiles_storage.path('json/todo.json'), 'w') as outfile:
        json.dump(dane, outfile)

def get_new_todo_task_id():
    with open(staticfiles_storage.path('json/todo.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    return int(list(dane.keys())[-1]) + 1

def delete_todo_task(todo_task_id):
    with open(staticfiles_storage.path('json/todo.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    del dane[todo_task_id]
    with open(staticfiles_storage.path('json/todo.json'), 'w') as outfile:
        json.dump(dane, outfile)

def get_dane_hurtownie_maile_wyslij_zestawienia():
    dane_hurtowni = slowniki.hurtownie_maile_wyslij_zestawienia
    pliki_pulpit_pdf = glob.glob(rf'C:\Users\tomas\Desktop\*.pdf')
    dane_zwrotne = []
    for f in pliki_pulpit_pdf:
        if '5472110371' in f or '129551' in f:
            hurtownia = f.split('_')[1]
            if hurtownia in dane_hurtowni.keys():
                dane_zwrotne.append({'hurtownia': hurtownia,
                                     'plik': f,
                                     'email': dane_hurtowni[hurtownia]})
    return dane_zwrotne

def wyslij_zestawienie_do_hurtowni(dane):
    text = 'Pozdrawiam' \
           '' \
           'Tomasz Zembok'

    mail = Maile.Maile()
    nazwa_pliku = dane['plik'].split('\\')[-1]
    data = nazwa_pliku.split("_")[2][0:4] + '-' + nazwa_pliku.split("_")[2][4:6] \
           + '-' + nazwa_pliku.split("_")[2][6:8]

    subject = f'{nazwa_pliku.split("_")[0]} - zestawienie do płatności ' \
              f'z dnia {data} - {nazwa_pliku.split("_")[3][0:-4]} zł'
    email_hurtowni = dane['email']
    zestawienie_folder = slowniki.foldery_zestawienia[dane['hurtownia']] + nazwa_pliku

    mail.mail_text_attachmen(email_hurtowni, subject, text, dane['plik'],
                             keyring.get_password("mejek_mail", "mejek_mail"))
    shutil.move(dane['plik'], zestawienie_folder)

def wyslij_prosbe_o_zestawienie():
    mail = Maile.Maile()
    subject = '5472110371 poproszę o zestawienie do patności'
    text = 'Pozdrawiam' \
           '' \
           'Tomasz Zembok'
    for key in slowniki.hurtownie_maile_pobierz_zestawienia:
        adres_email = slowniki.hurtownie_maile_pobierz_zestawienia[key]
        mail.mail_text(adres_email, subject, text,
                       keyring.get_password("mejek_mail", "mejek_mail"))

def wyslij_prosbe_o_dane_do_wyplaty():
    mail = Maile.Maile()
    subject = 'Proszę o dane do wypłaty'
    text = 'Pozdrawiam' \
           '' \
           'Tomasz Zembok'
    for key, mail_addres in slowniki.maile_apteki.items():
        mail.mail_text(mail_addres, subject, text, keyring.get_password("mejek_mail", "mejek_mail"))

def wyslij_prosbe_o_zakupy():
    mail = Maile.Maile()
    subject = 'Proszę o listę zakupów'
    text = 'Pozdrawiam' \
           '' \
           'Tomasz Zembok'
    for key, mail_addres in slowniki.maile_apteki.items():
        mail.mail_text(mail_addres, subject, text, keyring.get_password("mejek_mail", "mejek_mail"))

#SAGE
def get_lista_wyciagow(bank):
    with open(staticfiles_storage.path('json/sage_wyciagi.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    lista_wyciagow = []
    for key in dane:
        if bank in key:
            lista_wyciagow.append(key)

    lista_wyciagow = sorted(lista_wyciagow)
    lista_wyciagow.reverse()
    lista_wyboru_tuple = [('0','')]
    n = 1
    for w in lista_wyciagow:
        lista_wyboru_tuple.append((f'{n}',w))
        n+=1

    return(lista_wyboru_tuple)

def get_wyciag_key(wyciag_id, lista_wyboru):
    for w in lista_wyboru:
        if w[0] == wyciag_id:
            return w[1]
            break

def get_lista_wyboru_id(wyciag_key, lista_wyboru):
    for w in lista_wyboru:
        if w[1] == wyciag_key:
            return w[0]

def mt940_parser(plik):
    transactions = mt940.parse(plik)

    lista_zwrotna = []  # 0 - nr transakcji, 1 - data, 2 - tytuł, 3 - kontrahent, 4 - kwota, 5 - nip
    # 6 -konto_wn, 7 - konto_ma, 8 - id_sage, 9 - rachunek, 10 - konto specjalne, 11 - opis

    with open(staticfiles_storage.path('json/sage_kontrahenci_stali.json'), "r", encoding='utf-8') as json_file:
        kontrahenci_stali = json.load(json_file)

        nr_transakcji = 1
        for t in transactions:
            szczeguly = t.data['transaction_details'].split('\n')
            opis = szczeguly[0][6:]
            data_transakcji = t.data['date']
            tytul = ''
            nr_rachunku = ''
            kontrahent = szczeguly[14][3:]
            nip = ''
            id_sage = ''
            konto_wn = ''
            konto_ma = ''
            konto_specjalne = 'NIE'

            kwota = str(t.data['amount'])
            if '-' in kwota:
                kwota = kwota.replace('-', '')[:-4]
            else:
                kwota = kwota[:-4]

            if opis != 'PROWIZJA/OPŁATA' and opis != 'WPŁATA' and opis != 'PŁATNOŚĆ KARTĄ':
                index_dwukropwek = szczeguly[3].index(':') + 1
                nr_rachunku = szczeguly[3][index_dwukropwek:]
                tytul = szczeguly[4][3:] + szczeguly[5][3:] + szczeguly[6][3:] + szczeguly[7][3:]

            # rodzaj transakcji C - uznanie, D - obciążenie
            if t.data['status'] == 'D':
                rodzaj = 'MINUS'

                if opis == 'PROWIZJA/OPŁATA':
                    tytul = 'PROWIZJA/OPŁATA'
                    konto_wn = '404-3'
                    konto_ma = '136'

                if opis == 'PŁATNOŚĆ KARTĄ':
                    tytul = 'PŁATNOŚĆ KARTĄ - ZAKUP'
                    konto_wn = '202-'
                    konto_ma = '136'

                if opis == 'PRZELEW DO US':
                    if 'VAT-7' in tytul:
                        tytul = f'PODATEK - VAT-7 {tytul.split()[3]}/{tytul.split()[7][-2:]}'
                        konto_wn = '221-5'
                        konto_ma = '136'
                    elif 'PIT4' in tytul:
                        tytul = f'PODATEK - PIT-4 {tytul.split()[3]}/{tytul.split()[7][-2:]}'
                        konto_wn = '220-1'
                        konto_ma = '136'
                    elif 'CIT' in tytul:
                        tytul = f'PODATEK - CIT {tytul.split()[3]}/{tytul.split()[7][-2:]}'
                        konto_wn = '220-4'
                        konto_ma = '136'

                if opis == 'PRZELEW DO ZUS':
                    tytul = f'PRZELEW DO ZUS'
                    konto_wn = '220-2'
                    konto_ma = '136'

                if 'PRZEKSIĘGOWANIE VAT' in opis:
                    tytul = 'PRZEKIĘGOWANIE VAT'
                    konto_wn = '137'
                    konto_ma = '136'

                if opis == 'PRZELEW WYCHODZĄCY':
                    wynik_konto_spec = sprawdz_konto_spec(nr_rachunku)
                    if wynik_konto_spec != False:
                        konto_specjalne = 'TAK'
                        if nr_rachunku == '70116022020000000201154264' and float(kwota) > 6900:
                            tytul = f'NAJEM - MARIA KAPPEL-ZIOŁA {tytul}'
                            konto_wn = '202-135'
                            konto_ma = '136'
                        else:
                            tytul = wynik_konto_spec[0]
                            konto_wn = wynik_konto_spec[1]
                            konto_ma = str(wynik_konto_spec[2])

                    else:
                        nip_biala_lista = biala_lista.sprawdz_biala_lista_rachunek(nr_rachunku)
                        if nip_biala_lista != False:
                            nip = nip_biala_lista
                            if nip_biala_lista in kontrahenci_stali:
                                id_sage = kontrahenci_stali[f"{nip_biala_lista}"]["id_kontrahenta"]
                                if '(H)' in tytul:
                                    tytul = f'(H-{id_sage}): {tytul}'
                                else:
                                    tytul = f'{tytul}'
                                    kontrahent = kontrahenci_stali[f"{nip_biala_lista}"]["nazwa"]
                                konto_wn = f'202-{kontrahenci_stali[f"{nip_biala_lista}"]["id_kontrahenta"]}'
                                konto_ma = '136'
                            else:
                                print(f'Brak danych o kontach. Nazwa: {kontrahent}')
                                kontrahent = ''
                                konto_wn = '202-'
                                konto_ma = '136'
                        else:
                            if nr_rachunku == '51103015080000000819321000':
                                tytul = f'PPK PKO - {tytul}'
                                konto_wn = '233'
                                konto_ma = '136'

            if t.data['status'] == 'C':
                rodzaj = 'PLUS'

                if opis == 'WPŁATA':
                    tytul = 'WPŁATA GOTÓWKOWA'
                    konto_wn = '136'
                    konto_ma = '149'

                elif 'SOA/' in tytul or 'Z TYT. TRANSAKCJI KARTAMI' in tytul:
                    tytul = 'ZAPŁATA KARTĄ'
                    konto_wn = '136'
                    konto_ma = '145'

                elif 'PRZEKSIĘGOWANIE VAT' in opis:
                    tytul = 'PRZEKIĘGOWANIE VAT'
                    konto_wn = '136'
                    konto_ma = '137'

                elif 'PRZELEW PRZYCHODZĄCY' in opis:

                    nip_biala_lista = biala_lista.sprawdz_biala_lista_rachunek(nr_rachunku)
                    if nip_biala_lista != False:
                        nip = nip_biala_lista
                        if nip_biala_lista in kontrahenci_stali:
                            if nip_biala_lista == '5472110371':
                                konto_wn = '136'
                                konto_ma = '149'
                            else:
                                id_sage = kontrahenci_stali[f"{nip_biala_lista}"]["id_kontrahenta"]
                                kontrahent = kontrahenci_stali[f"{nip_biala_lista}"]["nazwa"]
                                konto_wn = '136'
                                konto_ma = f'200-{kontrahenci_stali[f"{nip_biala_lista}"]["id_kontrahenta"]}'

                        else:
                            print(f'Brak kontrahenta w bazie')
                            kontrahent = ''
                            konto_wn = '136'
                            konto_ma = f'200-'
                    else:
                        print(f'Brak danych o kontach. Nazwa: {kontrahent}')
                        konto_wn = '136'
                        konto_ma = f''

            lista_zwrotna.append([nr_transakcji, data_transakcji, tytul, kontrahent, kwota,
                                  nip, konto_wn, konto_ma, id_sage, nr_rachunku, konto_specjalne, rodzaj])
            nr_transakcji += 1

    return lista_zwrotna

def sprawdz_konto_spec(nr_rachunku):
    with open(staticfiles_storage.path('json/sage_konta_specjalne.json'), "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    if nr_rachunku in data:
        return [data[nr_rachunku]['tytul'], data[nr_rachunku]['konto_wn'], data[nr_rachunku]['konto_ma']]
    return False

def dodaj_konto_specjalne(konto, tytul, konto_wn, konto_ma):
    with open(staticfiles_storage.path('json/sage_konta_specjalne.json'), "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    if konto not in data.keys():
        data[konto] = {}
        data[konto]['tytul'] = tytul
        data[konto]['konto_wn'] = konto_wn
        data[konto]['konto_ma'] = konto_ma

        with open(staticfiles_storage.path('json/sage_konta_specjalne.json'), 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile)
        return True

    return False

def konto_specjalne_delete(konto):
    with open(staticfiles_storage.path('json/sage_konta_specjalne.json'), "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    del data[konto]

    with open(staticfiles_storage.path('json/sage_konta_specjalne.json'), 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)

def kontrahenci_stali_import_danych():
    with open(staticfiles_storage.path('json/sage_kontrahenci_stali.json'), "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    clipboard = Tk().clipboard_get().split('\n')

    for d in clipboard:
        if d != '':
            id_sage = d.split('\t')[1]
            nazwa = d.split('\t')[3]
            nip = d.split('\t')[4]
            if nip != '':
                if nip not in data:
                    data[nip] = {}

                data[nip]['nazwa'] = nazwa.strip('\n')
                data[nip]['id_kontrahenta'] = id_sage

    with open(staticfiles_storage.path('json/sage_kontrahenci_stali.json'), 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)

def pko_parser(plik):
    lista_zwrotna = []
    tree = ET.parse(plik)
    root = tree.getroot()

    with open(staticfiles_storage.path('json/sage_kontrahenci_stali.json'), "r", encoding='utf-8') as json_file:
        kontrahenci_stali = json.load(json_file)

        for elem in root.iter('operation'):

            # 0 - nr transakcji, 1 - data, 2 - tytuł, 3 - kontrahent, 4 - kwota, 5 - nip
            # 6 -konto_wn, 7 - konto_ma, 8 - id_sage, 9 - rachunek, 10 - konto specjalne, 11 - opis

            data_operacji = elem.find('exec-date').text
            kontrahent = ''
            kwota = (elem.find('amount').text).strip('-').strip('+')
            nip = ''
            konto_wn = ''
            konto_ma = ''
            id_sage = ''
            rachunek = ''
            konto_specjalne = 'NIE'
            opis_pm = ''

            rodzaj = elem.find('type').text

            if rodzaj == 'Opłata' or rodzaj == 'Prowizja':
                tytul = 'OPŁATA'
                konto_ma = '130'
                konto_wn = '404-3'
                opis_pm = 'MINUS'

            if rodzaj == 'Przelew na rachunek' or rodzaj == 'Przelew zagraniczny':
                opis = elem.find('description').text
                opis_new = opis.split('\n')
                opis_pm = 'PLUS'
                for n_opis in opis_new:
                    nn = n_opis.split(': ')
                    if nn[0] == 'Rachunek nadawcy':
                        rachunek = nn[1].replace(' ', '')
                    if nn[0] == 'Nazwa nadawcy':
                        kontrahent = nn[1]
                    if nn[0] == 'Tytuł':
                        tytul = nn[1]

                if 'ŚLĄSKI ODDZIAŁ WOJEWÓDZKI' in kontrahent:
                    tytul = f'NFZ: {tytul}'
                    kontrahent = 'NFZ'
                    konto_wn = '130'
                    konto_ma = '200-11'

                elif rachunek == '73102013900000610205981081':
                    tytul = f'ZWROT Z KONTA VAT'
                    konto_wn = '130'
                    konto_ma = '134'

                else:
                    nip_biala_lista = biala_lista.sprawdz_biala_lista_rachunek(rachunek)
                    nip = nip_biala_lista
                    if nip_biala_lista in kontrahenci_stali:
                        id_sage = kontrahenci_stali[f"{nip_biala_lista}"]["id_kontrahenta"]
                        kontrahent = kontrahenci_stali[f"{nip_biala_lista}"]["nazwa"]
                        konto_wn = '130'
                        konto_ma = f'200-{kontrahenci_stali[f"{nip_biala_lista}"]["id_kontrahenta"]}'
                        tytul = f'{kontrahent} - {tytul}'

                    else:
                        print(f'Brak kontrahenta w bazie')
                        kontrahent = ''
                        konto_wn = '136'
                        konto_ma = f'200-'

            if rodzaj == 'Przelew z rachunku' or rodzaj == 'Przelew podatkowy':
                opis = elem.find('description').text
                opis_new = opis.split('\n')
                opis_pm = 'MINUS'
                for n_opis in opis_new:
                    nn = n_opis.split(': ')
                    if nn[0] == 'Rachunek odbiorcy':
                        rachunek = nn[1].replace(' ', '')
                    if nn[0] == 'Nazwa odbiorcy':
                        kontrahent = nn[1]
                    if nn[0] == 'Tytuł':
                        tytul = nn[1]
                    if nn[0] == 'Symbol formularza':
                        symbol_form = nn[1]
                    if nn[0] == 'Okres płatności':
                        okres_form = nn[1]
                    if nn[0] == 'Numer faktury VAT lub okres płatności zbiorczej':
                        opis_vat_split = nn[1]

                if rodzaj == 'Przelew podatkowy':
                    tytul = f'PODATEK - {symbol_form} {okres_form} {kontrahent}'
                    if 'VAT' in symbol_form:
                        konto_wn = '221-5'
                    else:
                        konto_wn = ''
                    konto_ma = '130'

                elif rachunek == "73102013900000610205981081":
                    tytul = f'PRZELEW VAT SPLIT PAYMENT'
                    konto_wn = '134'
                    konto_ma = '130'

                elif rachunek == "71116022020000000469095212":
                    tytul = f'PRZELEW ŚRODKÓW WŁASNYCH'
                    konto_ma = '130'
                    konto_wn = '149'

            lista_zwrotna.append([data_operacji, tytul, kontrahent, kwota, nip,
                                  konto_wn, konto_ma, id_sage, rachunek, konto_specjalne, opis_pm])

    lista_zwrotna.reverse()
    n = 1
    for l in lista_zwrotna:
        l.insert(0, n)
        n += 1

    return lista_zwrotna

def dodaj_wyciag(dane_do_wyciagu, plik):

    id_wyciag = plik

    with open(staticfiles_storage.path('json/sage_wyciagi.json'), "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    if id_wyciag not in data:
        data[id_wyciag] = {}

    for dane in dane_do_wyciagu:
        if dane[0] not in data[id_wyciag]:
            data[id_wyciag][f"{dane[0]}"] = {}

        dane_transakcji = {'data': str(dane[1]), 'tytul': dane[2], 'kontrahent': dane[3],
                           'kwota': dane[4], 'nip': dane[5], 'konto_wn': dane[6], 'konto_ma': dane[7],
                           'id_sage': dane[8], 'rachunek': dane[9], 'konto_spec': dane[10], 'rodzaj': dane[11]}
        data[id_wyciag][f"{dane[0]}"] = dane_transakcji

    with open(staticfiles_storage.path('json/sage_wyciagi.json'), 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)

def get_dane_pozycja_wyciag(id_wyciag, id_pozycja):
    with open(staticfiles_storage.path('json/sage_wyciagi.json'), "r", encoding='utf-8') as json_file:
        wyciag_json = json.load(json_file)

    return wyciag_json[id_wyciag][id_pozycja]

def zapisz_dane_pozycja_wyciag(id_wyciag, id_pozycja, dane):
    with open(staticfiles_storage.path('json/sage_wyciagi.json'), "r", encoding='utf-8') as json_file:
        wyciag_json = json.load(json_file)

    wyciag_json[id_wyciag][id_pozycja] = dane

    with open(staticfiles_storage.path('json/sage_wyciagi.json'), 'w', encoding='utf-8') as outfile:
        json.dump(wyciag_json, outfile)

def eksportuj_wyciag_do_sage(wyciag_key_ekport):

    wyciag_lista = get_dane_wyciag_eksport(wyciag_key_ekport)

    ahk = AHK(executable_path=r"C:\Program Files\AutoHotkey\AutoHotkey.exe")
    lista_okien = list(ahk.windows())
    for okno in lista_okien:
        if 'Symfonia Finanse' in str(okno.title):
            okno.activate()
            sleep(1)
            break
    sleep(1)
    ahk.click(208, 210)

    for n in wyciag_lista:
        sleep(0.3)
        ahk.type(n[0])
        ahk.key_press('ENTER')
        ahk.key_press('ENTER')
        os.system(f"echo {n[1].strip('&')} | clip")
        ahk.send_input('^v')
        ahk.key_press('ENTER')
        ahk.key_press('ENTER')
        ahk.type(f'{n[2]}')
        ahk.key_press('ENTER')
        if n[3] != '':
            ahk.type(f'{n[3]}')
        ahk.key_press('ENTER')
        ahk.key_press('ENTER')
        ahk.type(f'{n[4]}')
        ahk.key_press('ENTER')

def get_dane_wyciag_eksport(id_wyciag):
    wyciag_lista = []
    with open(staticfiles_storage.path('json/sage_wyciagi.json'), "r", encoding='utf-8') as json_file:
        wyciag_json = json.load(json_file)

    wyciag = wyciag_json[id_wyciag]
    for k in wyciag:
        wyciag_lista.append([wyciag[k]['data'], wyciag[k]['tytul'], wyciag[k]['kwota'],
                             wyciag[k]['konto_wn'], wyciag[k]['konto_ma']])
    return wyciag_lista

def faktury_wykaz_get_dostawcy():
    query = f'SELECT id, nazwa FROM dostawcy WHERE id > 18 ORDER BY nazwa'
    wynik = zpt_queries.zpt_query_fetchall(query)
    wynik = ((0,''), *wynik) # dodawanie pustego pola do tupli, fajny sposób od python 3.5
    return wynik

def faktury_wykaz_get_kontrahenci():
    query = f'SELECT id_kont, nazwa FROM platnosci_kontrahenci ORDER BY nazwa'
    wynik = zpt_queries.zpt_query_fetchall(query)
    wynik = ((0,''), *wynik) # dodawanie pustego pola do tupli, fajny sposób od python 3.5
    return wynik

def sage_rf_pliki_set_miesiac():
    rok = datetime.today().year
    miesiac = datetime.today().month - 1
    if miesiac == 0:
        miesiac = 12
        rok = rok - 1
    elif miesiac < 10:
        miesiac = f'0{miesiac}'
    else:
        pass
    return f'{rok}-{miesiac}'

def sage_rf_pliki_eksport(id_apteka, okres):
    raport_eksportu = ''
    text_start = '''INFO{
            	Nazwa programu =Mejek_konwerter
            	Wersja szablonu =4
            	dane_z_oddzialu =1
            	Kontrahent{
            	}
            }
            '''

    raport_eksportu += f'Apteka: {slowniki.apteki_id_nazwa[id_apteka]}</br>'

    pulpit = r'C:\Users\tomas\Desktop'
    if len(glob.glob(f'{pulpit}\*.dbf')) != 0:
        plik = glob.glob(f'{pulpit}\*.dbf')[0]
        # GENERACJA PLIKU FBP (faktury bez paragonu - dla firm)
        txt_FBP = fr'C:\Users\tomas\Desktop\0{id_apteka}_FBP_20{plik[-10:-4]}.txt'
        opis_FBP = 'sprzedaż leków FV'
        konto_WN_FBP = 145

        dbf = Dbf5(plik, codec='mazovia')
        db = dbf.to_dataframe()

        db_list = db.values.tolist()
        with open(txt_FBP, 'w') as file:
            file.write(text_start)
            for p in db_list:
                if p[2] == 'FSV' and str(p[60]) == 'nan':
                    file.write(set_text_dokument_FBP(p, opis_FBP, konto_WN_FBP, id_apteka))
        shutil.move(txt_FBP,
                    fr'C:\Users\tomas\Dysk Google\IMPORTY\00_FBP\0{id_apteka}_FBP_20{plik[-10:-4]}.txt')

        # GENERACJA PLIKU FPAR (faktury z paragonem)
        txt_FPAR = fr'C:\Users\tomas\Desktop\0{id_apteka}_FPAR_20{plik[-10:-4]}.txt'
        opis_FPAR = 'sprzedaż lekarstw'
        konto_WN_FPAR = 145
        with open(txt_FPAR, 'w') as file:
            file.write(text_start)
            for p in db_list:
                if p[2] == 'FSV' and str(p[60]) != 'nan':
                    file.write(set_text_dokument_FPAR(p, opis_FPAR, konto_WN_FPAR, id_apteka))
        shutil.move(txt_FPAR,
                    fr'C:\Users\tomas\Dysk Google\IMPORTY\00_FPAR\0{id_apteka}_FBP_20{plik[-10:-4]}.txt')

        # GENERACJA PLIKU TOW (zakupy i korekty) - razem ze sprawdzeniem)
        txt_TOW = fr'C:\Users\tomas\Desktop\0{id_apteka}_TOW_20{plik[-10:-4]}.txt'
        query = f'SELECT dane FROM fv_sage WHERE apteka = {id_apteka} AND data_akt = "{okres}"'
        wynik_querry = zpt_queries.zpt_query_fetchone(query)[0]
        dane = json.loads(wynik_querry, encoding='utf-8')

        zpt_zakupy = []
        zpt_korekty = []

        i = 0
        for n in dane['Z']:
            zpt_zakupy.append(dane['Z'][f'{n}']['nr_faktury'])
        for n in dane['K']:
            zpt_korekty.append(dane['K'][f'{n}']['nr_faktury'])

        # get lista fakrut z kamsoft fp
        kamsoft_zakupy = []
        kamsoft_korekty = []

        for p in db_list:
            if p[2] == 'FZV' and float(p[23]) != 0:
                kamsoft_zakupy.append(p[8])
            if p[2] == 'KZV' and float(p[23]) != 0:
                kamsoft_korekty.append(p[8])

        # porownanie ilości elementów
        if len(kamsoft_zakupy) == len(zpt_zakupy):
            raport_eksportu += f'\tLiczba elementów obu tablic ZAKUPÓW: {len(kamsoft_zakupy)}</br>'
        else:
            raport_eksportu += f'\tBŁĄD. Tablica kamsoft zakupy:'\
                                f' {len(kamsoft_zakupy)}, tablica zpt zakupy:'\
                                f' {len(zpt_zakupy)}</br>'

        if len(kamsoft_korekty) == len(zpt_korekty):
            raport_eksportu += f'\tLiczba elementów obu tablic KOREKT: {len(kamsoft_korekty)}</br>'
        else:
            raport_eksportu += f'\tBŁĄD. Tablica kamsoft korekty:'\
                                             f' {len(kamsoft_korekty)}, tablica zpt korekty:'\
                                             f' {len(zpt_korekty)}</br>'

        # sprawdzenie elementow
        zakupy_braki = []
        korekty_braki = []

        for f in kamsoft_zakupy:
            if f not in zpt_zakupy:
                zakupy_braki.append(f)
        for f in kamsoft_korekty:
            if f not in zpt_korekty:
                korekty_braki.append(f)

        if zakupy_braki != []:
            raport_eksportu +=  f'\tBŁĄD. Brak faktur {zakupy_braki}</br>'

        else:
            raport_eksportu += f'\tWszystkie faktury zakupu są zapisane w ZPT</br>'

        if korekty_braki != []:
            raport_eksportu += f'\tBŁĄD. Brak faktur {korekty_braki}</br>'

        else:
            raport_eksportu += f'\tWszystkie faktury korekty są zapisane w ZPT</br>'

        with open(txt_TOW, 'w') as file:
            file.write(text_start)
            n = 1
            for fv in zpt_zakupy:
                for p in db_list:
                    if p[8] == fv:
                        if p[2] == 'FZV' or p[2] == 'KZV' and set_text_dokument_TOW(p, id_apteka,
                                                                                         'zakup') != False:
                            file.write(set_text_dokument_TOW(p, id_apteka, 'zakup'))
                            raport_eksportu += f'\t\tTOW_ZAKUPY_{n}: {p[8]}</br>'
                            n += 1
                            break

            n = 1
            for fv in zpt_korekty:
                for p in db_list:
                    if p[8] == fv:
                        if p[2] == 'FZV' or p[2] == 'KZV' and set_text_dokument_TOW(p, id_apteka,
                                                                                         'korekta') != False:
                            file.write(set_text_dokument_TOW(p, id_apteka, 'korekta'))
                            raport_eksportu +=  f'\t\tTOW_KOREKTY_{n}: {p[8]}</br>'
                            n += 1
                            break

        shutil.move(txt_TOW,
                    fr'{slowniki.apteki_id_rf_to_sage[f"{id_apteka}"]["folder"]}\0{id_apteka}_TOW_20{plik[-10:-4]}.txt')

    return raport_eksportu

def set_text_dokument_FBP(row, opis, konto_WN, apteka_id):
    if str(row[58]) == 'nan': nip = ''
    konto_MA = slowniki.apteki_id_rf_to_sage[f'{apteka_id}']['konto_MA']

    text_dokument = f'''Kontrahent{{
    id ={row[58]}
    info =N
    kod ={row[55]}
    nazwa ={row[55]}
    miejscowosc ={row[56].split(' ')[-1]}
    ulica ={row[56].split(' ')[0] + ' ' + row[56].split(' ')[1]}
    nip ={row[58]}
    VIES =0
    krajKod =PL
    osfiz =0
    kraj{{
        symbol =PL
    }}
}}
Dokument{{
    rodzaj_dok =sprzedaży
    dozaplaty ={row[23]:.2f}
    wdozaplaty ={row[23]:.2f}
    FK nazwa ={row[8]}
    opis FK ={opis} 
    mppFlags =0
    kwota ={row[23]:.2f}
    obsluguj jak =FVS
    symbol FK =FVS
    dataWystawienia ={str(row[4])}
    datawpl ={row[4]}
    dataSprzedazy ={row[4]}
    kod ={row[8]}
    plattermin ={row[6]}
    rejestr_platnosci =BANK
    forma_platnosci =przelew
    Dane Nabywcy{{
        khid ={row[58]}
        khnazwa ={row[55]}
        khulica ={row[56].split(' ')[0] + ' ' + row[56].split(' ')[1]}
        khmiasto ={row[56].split(' ')[-1]}
        khnip ={row[58]}
    }}
    Zapis{{
        strona =WN
        kwota ={row[23]:.2f}
        konto ={konto_WN}
        IdDlaRozliczen =1
        pozycja =0
        ZapisRownolegly =0
        NumerDok ={row[8]}
        opis ={opis}
    }}
    Zapis{{
        strona =MA
        pozycja =0
        ZapisRownolegly =0
        IdDlaRozliczen =2
        kwota ={row[24]:.2f}
        konto ={konto_MA}
        NumerDok ={row[8]}
    }}
    Zapis{{
        strona =MA
        pozycja =0
        ZapisRownolegly =0
        IdDlaRozliczen =3
        kwota ={row[25]:.2f}
        konto =221-2
        opis ={opis}
        NumerDok ={row[8]}
    }}
    '''

    text_dokument += f'''Rejestr{{
        Skrot =rSPV
        Nazwa =Sprzedaż VAT
        ABC =1
        okres ={str(row[4])[:7] + '-01'}
        stawka =23.00
        brutto ={(float(row[65]) + float(row[73])):.2f}
        netto ={row[65]:.2f}
        VAT ={row[73]:.2f}
    }}
    '''

    text_dokument += f'''Rejestr{{
        Skrot =rSPV
        Nazwa =Sprzedaż VAT
        ABC =1
        okres ={str(row[4])[:7] + '-01'}
        stawka =8.00
        brutto ={(float(row[66]) + float(row[74])):.2f}
        netto ={row[66]:.2f}
        VAT ={row[74]:.2f}
    }}
    '''

    text_dokument += f'''Rejestr{{
        Skrot =rSPV
        Nazwa =Sprzedaż VAT
        ABC =1
        okres ={str(row[4])[:7] + '-01'}
        stawka =5.00
        brutto ={(float(row[67]) + float(row[75])):.2f}
        netto ={row[67]:.2f}
        VAT ={row[75]:.2f}
    }}
    '''

    text_dokument += f'''Rejestr{{
            Skrot =rSPV
            Nazwa =Sprzedaż VAT
            ABC =1
            okres ={str(row[4])[:7] + '-01'}
            stawka =0.00
            brutto ={row[68]:.2f}
            netto ={row[68]:.2f}
            VAT =0.00
        }}
        '''

    text_dokument += f'''Transakcja{{
        IdDlaRozliczen =1
        kwota ={row[23]:.2f}
        termin ={row[6]}
    }}
}}
'''
    return text_dokument

def set_text_dokument_FPAR(row, opis, konto_WN, apteka_id):
    if str(row[58]) != 'nan':
        nip = f'nip ={row[58]}\n'
        khnip = f'nip ={row[58]}\n'
    else:
        nip = ''
        khnip = ''

    nazwa_zastepcza = ''
    if row[55] == 'B╒HM KLAUDIA':
        nazwa_zastepcza = 'BOHM KLAUDIA'
    else:
        nazwa_zastepcza = row[55]

    konto_MA = slowniki.apteki_id_rf_to_sage[f'{apteka_id}']['konto_MA']
    print(nazwa_zastepcza)
    text_dokument = f'''Kontrahent{{
    id ={nazwa_zastepcza}
    info =N
    kod ={nazwa_zastepcza}
    nazwa ={nazwa_zastepcza}
    miejscowosc ={row[56].split(' ')[-1]}
    ulica ={row[56].split(' ')[0] + ' ' + row[56].split(' ')[1]}
    {nip}
    VIES =0
    krajKod =PL
    osfiz =0
    kraj{{
        symbol =PL
    }}
}}
Dokument{{
    rodzaj_dok =sprzedaży
    dozaplaty ={row[23]:.2f}
    wdozaplaty ={row[23]:.2f}
    FK nazwa ={row[8]}
    opis FK ={opis} 
    mppFlags =0
    kwota ={row[23]:.2f}
    obsluguj jak =FVS
    symbol FK =FVS
    dataWystawienia ={row[4]}
    datawpl ={row[4]}
    dataSprzedazy ={row[4]}
    kod ={row[8]}
    plattermin ={row[6]}
    rejestr_platnosci =BANK
    forma_platnosci =przelew
    Dane Nabywcy{{
        khid ={nazwa_zastepcza.replace(' ', '')}
        khnazwa ={nazwa_zastepcza}
        khulica ={row[56].split(' ')[0] + ' ' + row[56].split(' ')[1]}
        khmiasto ={row[56].split(' ')[-1]}
        {khnip}
    }}
    Zapis{{
        strona =WN
        kwota ={row[23]:.2f}
        konto ={konto_WN}
        IdDlaRozliczen =1
        pozycja =0
        ZapisRownolegly =0
        NumerDok ={row[8]}
        opis ={opis}
    }}
    Zapis{{
        strona =MA
        pozycja =0
        ZapisRownolegly =0
        IdDlaRozliczen =2
        kwota ={row[24]:.2f}
        konto ={konto_MA}
        NumerDok ={row[8]}
    }}
    Zapis{{
        strona =MA
        pozycja =0
        ZapisRownolegly =0
        IdDlaRozliczen =3
        kwota ={row[25]:.2f}
        konto =221-2
        opis ={opis}
        NumerDok ={row[8]}
    }}
    '''

    text_dokument += f'''Rejestr{{
        Skrot =rSPV
        Nazwa =Sprzedaż VAT
        ABC =1
        okres ={str(row[4])[:7] + '-01'}
        stawka =23.00
        brutto ={(float(row[65]) + float(row[73])):.2f}
        netto ={row[65]:.2f}
        VAT ={row[73]:.2f}
    }}
    '''

    text_dokument += f'''Rejestr{{
        Skrot =rSPV
        Nazwa =Sprzedaż VAT
        ABC =1
        okres ={str(row[4])[:7] + '-01'}
        stawka =8.00
        brutto ={(float(row[66]) + float(row[74])):.2f}
        netto ={row[66]:.2f}
        VAT ={row[74]:.2f}
    }}
    '''

    text_dokument += f'''Rejestr{{
        Skrot =rSPV
        Nazwa =Sprzedaż VAT
        ABC =1
        okres ={str(row[4])[:7] + '-01'}
        stawka =5.00
        brutto ={(float(row[67]) + float(row[75])):.2f}
        netto ={row[67]:.2f}
        VAT ={row[75]:.2f}
    }}
    '''

    text_dokument += f'''Rejestr{{
            Skrot =rSPV
            Nazwa =Sprzedaż VAT
            ABC =1
            okres ={str(row[4])[:7] + '-01'}
            stawka =0.00
            brutto ={row[68]:.2f}
            netto ={row[68]:.2f}
            VAT =0.00
        }}
        '''

    text_dokument += f'''Transakcja{{
        IdDlaRozliczen =1
        kwota ={row[23]:.2f}
        termin ={row[6]}
    }}
}}
'''
    return text_dokument

def set_text_dokument_TOW(row, apteka_id, rodzaj):
    symbol_FK = ''
    opis = ''
    nazwa_kor = ''
    data_kor = ''
    miejscowosc = ''
    opis_ZAKUP = 'Zakup towaru'
    opis_ZWROT = 'zwrot towaru'

    if float(row[23]) == 0:
        return False
    if rodzaj == 'zakup':
        symbol_FK = 'FVZ'
        opis = opis_ZAKUP
        nazwa_kor = ''
        data_kor = ''
    if rodzaj == 'korekta':
        opis = opis_ZWROT
        symbol_FK = 'FKZ'
        nazwa_kor = f'\nNazwaKor ={row[9]}\n'
        data_kor = f'DataKor ={row[6]}\n'

    if len(row[56].split(' ')) == 4:
        miejscowosc = f'{row[56].split(" ")[-2]} {row[56].split(" ")[-1]}, {row[56].split(" ")[0] + " " + row[56].split(" ")[1]}'
    elif row[56].split(' ')[0] == 'Kolista':
        miejscowosc = f'{row[56].split(" ")[-2]} {row[56].split(" ")[-1]}, {row[56].split(" ")[0] + " " + row[56].split(" ")[2]}'
    elif row[56].split(' ')[0] == 'DUBLIN':
        miejscowosc = f'{row[56].split(" ")[0]}'
    else:
        miejscowosc = ''

    text_dokument = f'''Kontrahent{{
    id ={row[58].replace(' ', '').replace('-', '')}
    info =N
    kod ={row[55]}
        nazwa ={row[55]}
        miejscowosc ={miejscowosc}
        nip ={row[58].replace(' ', '').replace('-', '')}
    VIES =0
    krajKod =PL
    osfiz =0
    kraj{{
        symbol =PL
    }}
}}
Dokument{{
    rodzaj_dok =zakupu
    dozaplaty ={row[23]:.2f}
    wdozaplaty ={row[23]:.2f}
    FK nazwa ={row[8]}
    opis FK ={opis} 
    mppFlags =0
    kwota ={row[23]:.2f}
    obsluguj jak =FVZ
    symbol FK ={symbol_FK}
    dataWystawieniaObca ={row[4]}
    datawpl ={row[5]}
    dataZakupu ={row[5]}
    kod ={row[8]}
    plattermin ={row[4]}
    rejestr_platnosci =BANK
    forma_platnosci =przelew{nazwa_kor}{data_kor}
    Dane Nabywcy{{
        khid ={row[58].replace(' ', '').replace('-', '')}
        khnazwa ={row[55]}
        khmiasto ={miejscowosc}
        khnip ={row[58].replace(' ', '').replace('-', '')}
    }}
    Zapis{{
        strona =WN
        pozycja =0
        ZapisRownolegly =0
        IdDlaRozliczen =2
        kwota ={row[24]:.2f}
        konto =330-{apteka_id}    
        NumerDok ={row[8]}
    }}
    Zapis{{
        strona =MA
        kwota ={row[23]:.2f}
        konto =202-K{row[58].replace(' ', '').replace('-', '')}
        IdDlaRozliczen =1
        pozycja =0
        ZapisRownolegly =0
        NumerDok ={row[8]}
        opis ={opis}
    }}
    Zapis{{
        strona =WN
        pozycja =0
        ZapisRownolegly =0
        IdDlaRozliczen =3
        kwota ={row[25]:.2f}
        konto =221-1
        opis ={opis}
        NumerDok ={row[8]}
    }}
    '''

    text_dokument += f'''Rejestr{{
        Skrot =rZPV
        Nazwa =Zakup VAT
        ABC =1
        okres ={str(row[5])[:7] + '-01'}
        stawka =23.00
        brutto ={(float(row[65]) + float(row[73])):.2f}
        netto ={row[65]:.2f}
        VAT ={row[73]:.2f}
    }}
    '''

    text_dokument += f'''Rejestr{{
        Skrot =rZPV
        Nazwa =Zakup VAT
        ABC =1
        okres ={str(row[5])[:7] + '-01'}
        stawka =8.00
        brutto ={(float(row[66]) + float(row[74])):.2f}
        netto ={row[66]:.2f}
        VAT ={row[74]:.2f}
    }}
    '''

    text_dokument += f'''Rejestr{{
        Skrot =rZPV
        Nazwa =Zakup VAT
        ABC =1
        okres ={str(row[5])[:7] + '-01'}
        stawka =5.00
        brutto ={(float(row[67]) + float(row[75])):.2f}
        netto ={row[67]:.2f}
        VAT ={row[75]:.2f}
    }}
    '''

    text_dokument += f'''Rejestr{{
            Skrot =rZPV
            Nazwa =Zakup VAT
            ABC =1
            okres ={str(row[5])[:7] + '-01'}
            stawka =0.00
            brutto ={row[68]:.2f}
            netto ={row[68]:.2f}
            VAT =0.00
        }}
        '''

    text_dokument += f'''Transakcja{{
        IdDlaRozliczen =1
        kwota ={row[23]:.2f}
        termin ={row[6]}
    }}
}}
'''
    return str(text_dokument)





