import requests
import datetime
from . import zpt_queries

def sprawdz_biala_lista(nip, konto):
    data_param = datetime.date.today()
    konto_26 = konto.replace(' ', '')
    nip_9 = nip.replace(' ', '').replace('-', '')
    dane = requests.get(f'https://wl-api.mf.gov.pl/api/check/nip/{nip_9}/bank-account/{konto_26}?date={data_param}')
    dane = dane.json()
    print(dane)
    return dane

def sprawdz_biala_lista_rachunek(konto):
    data_param = datetime.date.today()
    konto_26 = konto.replace(' ', '')
    dane = requests.get(f'https://wl-api.mf.gov.pl/api/search/bank-account/{konto_26}?date={data_param}')
    dane = dane.json()
    if 'result' not in dane.keys():
        print('BRAK DANYCH W BIAŁEJ LIŚCIE A')
        return False

    if dane['result']['subjects'] == []:
        print('BRAK DANYCH W BIAŁEJ LIŚCIE B')
        return False

    elif 'result' in dane and dane['result']['subjects'] != []:
        nip = dane['result']['subjects'][0]['nip']
        return nip


def zapisz_sprawdzenie_biala_lista(nazwa, konto, nip):
    dane_bl = sprawdz_biala_lista(nip, konto)

    if 'result' in str(dane_bl):
        if dane_bl['result']['accountAssigned'] == 'TAK':
            status = dane_bl['result']['accountAssigned']
            czas = dane_bl['result']['requestDateTime']
            id_potw = dane_bl['result']['requestId']

            query = f'INSERT INTO biala_lista(czas, nazwa, konto, nip, status, kod_potw)' \
                    f' VALUES("{czas}", "{nazwa}", "{konto}", "{nip}", "{status}", "{id_potw}")'
            zpt_queries.zpt_query_modify(query)

    else:
        print('Bląd Biała Lista')
