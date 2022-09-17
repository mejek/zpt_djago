from . import zpt_queries
from . import slowniki
from . import funkcje_pomocnicze as fp
import datetime
from dateutil import easter
import json
from django.contrib.staticfiles.storage import staticfiles_storage
import pdfkit

# TABELE I DANE DO STRONY ONLINE #
def get_dane_obroty_dzienne():
    obroty_dzienne_dict = {}
    all_pacjenci = 0
    all_brutto = 0
    all_netto = 0
    all_zysk = 0
    all_magazyn = 0

    for n in range(2, 9):
        if n == 3:
            continue
        guerry_obroty_dzienne = f'SELECT * FROM obroty_dzienne WHERE' \
                                f' data = "{datetime.datetime.now().date()}"' \
                                f' AND apteka = {n}'
        obroty_dzienne_dane = zpt_queries.zpt_query_fetchall(guerry_obroty_dzienne)
        querry_magazyn_apteka = f'SELECT sum(cena_zak*ilakt) FROM rem_0{n}'
        magazyn_apteka = zpt_queries.zpt_query_fetchone(querry_magazyn_apteka)[0]

        magazyn = round(magazyn_apteka, 2)

        if not obroty_dzienne_dane:
            obroty_dzienne_dict[f'{n}'] = [0, 0, 0, 0, magazyn, slowniki.online_id_nazwa[f'{n}']]
            all_magazyn += magazyn

        else:
            obroty_dzienne_dict[f'{n}'] = [obroty_dzienne_dane[0][2],
                                           obroty_dzienne_dane[0][3],
                                           obroty_dzienne_dane[0][4],
                                           obroty_dzienne_dane[0][5],
                                           magazyn,
                                           slowniki.online_id_nazwa[f'{n}']]

            all_pacjenci += obroty_dzienne_dane[0][2]
            all_brutto += obroty_dzienne_dane[0][3]
            all_netto += obroty_dzienne_dane[0][4]
            all_zysk += obroty_dzienne_dane[0][5]
            all_magazyn += magazyn

    obroty_dzienne_dict[f'razem'] = [all_pacjenci, round(all_brutto, 2),
                                     round(all_netto, 2), round(all_zysk, 2),
                                     round(all_magazyn, 2), 'RAZEM']

    return obroty_dzienne_dict

def get_dane_obroty_miesieczne():
    obroty_miesieczne_dict = {}
    all_pacjenci = 0
    all_brutto = 0
    all_netto = 0
    all_zysk = 0

    for n in range(2, 9):
        if n == 3:
            continue
        guerry_obroty_miesieczne = f'SELECT SUM(pacjenci), SUM(obrot_brutto), SUM(obrot_netto),' \
                                   f' SUM(zysk_netto)' \
                                   f' FROM obroty_dzienne' \
                                   f' WHERE (data between  DATE_FORMAT(NOW() ,"%Y-%m-01") AND NOW())' \
                                   f' AND apteka = {n}'
        obroty_miesieczne_dane = zpt_queries.zpt_query_fetchall(guerry_obroty_miesieczne)
        if obroty_miesieczne_dane == ((None, None, None, None),):
            obroty_miesieczne_dict[f'{n}'] = [0, 0, 0, 0, 0, slowniki.online_id_nazwa[f'{n}']]

        else:
            # print(obroty_miesieczne_dane)
            marza = round((obroty_miesieczne_dane[0][3] / obroty_miesieczne_dane[0][2]) * 100, 2)
            obroty_miesieczne_dict[f'{n}'] = [int(obroty_miesieczne_dane[0][0]),
                                              round(obroty_miesieczne_dane[0][1], 2),
                                              round(obroty_miesieczne_dane[0][2], 2),
                                              round(obroty_miesieczne_dane[0][3], 2),
                                              marza,
                                              slowniki.online_id_nazwa[f'{n}']]
            all_pacjenci += obroty_miesieczne_dane[0][0]
            all_brutto += obroty_miesieczne_dane[0][1]
            all_netto += obroty_miesieczne_dane[0][2]
            all_zysk += obroty_miesieczne_dane[0][3]
        if all_netto != 0:
            marza_all = round((all_zysk / all_netto) * 100, 2)
        else:
            marza_all = 0
        obroty_miesieczne_dict[f'razem'] = [int(all_pacjenci), round(all_brutto, 2),
                                            round(all_netto, 2), round(all_zysk, 2),
                                            round(marza_all, 2), 'RAZEM']
    return obroty_miesieczne_dict

def tabela_obroty(dane, obroty):
    ostatnia_kolumna = ''
    jednostka = ''
    if obroty == 'dzienne':
        ostatnia_kolumna = 'STAN MAGAZYNOWY'
        jednostka = 'zł'
    elif obroty == 'miesieczne':
        ostatnia_kolumna = 'MARŻA'
        jednostka = '%'

    tabela_header = f'<table width=100% style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" >' \
                    f'<tr>' \
                    f'<td width=16%  class="td_obroty" ><b>APTEKA</b></td>' \
                    f'<td width=16%  class="td_obroty"><b>PACJENCI</b></td>' \
                    f'<td width=16% class="td_obroty"><b>OBRÓT BRUTTO</b></td>' \
                    f'<td width=16% class="td_obroty"><b>OBRÓT NETTO</b></td>' \
                    f'<td width=16% class="td_obroty"><b>ZYSK NETTO</b></td>' \
                    f'<td width=20% class="td_obroty"><b>{ostatnia_kolumna}</b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for n in range(2, 9):
        if n == 3:
            continue
        else:
            tabela_dane += f'<tr style="font-size: 12px;">' \
                           f'<td width=16%  class="td_obroty" >{dane[str(n)][5]}</td>' \
                           f'<td width=16%  class="td_obroty" >{dane[str(n)][0]}</td>' \
                           f'<td width=16%  class="td_obroty" >{fp.currency_format(dane[str(n)][1])} zł</td>' \
                           f'<td width=16%  class="td_obroty" >{fp.currency_format(dane[str(n)][2])} zł</td>' \
                           f'<td width=16%  class="td_obroty" >{fp.currency_format(dane[str(n)][3])} zł</td>' \
                           f'<td width=20%  class="td_obroty" >' \
                           f'{fp.currency_format(dane[str(n)][4])} {jednostka}</td>' \
                           '</tr>'

    dane_razem = dane['razem']
    tabela_razem = f'<tr style = "background-color: #c34f4f; font-size:14px;">' \
                   f'<td width=16%  class="td_obroty" ><b>{dane_razem[5]}</b></td>' \
                   f'<td width=16%  class="td_obroty" ><b>{dane_razem[0]}</b></td>' \
                   f'<td width=16%  class="td_obroty" ><b>{fp.currency_format(dane_razem[1])} zł</b></td>' \
                   f'<td width=16%  class="td_obroty" ><b>{fp.currency_format(dane_razem[2])} zł</b></td>' \
                   f'<td width=16%  class="td_obroty" ><b>{fp.currency_format(dane_razem[3])} zł</b></td>' \
                   f'<td width=20%  class="td_obroty" ><b>' \
                   f'{fp.currency_format(dane_razem[4])} {jednostka}</b></td>' \
                   '</tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_razem + tabela_zakonczenie

    return tabela_koncowa

def get_dane_prognoza():
    query = f'SELECT dane_prognoza FROM prognoza ORDER BY data DESC LIMIT 1'
    wynik = zpt_queries.zpt_query_fetchone(query)[0]
    # print(wynik)
    dane = json.loads(wynik)
    return dane

def tabela_prognoza(dane):
    tabela_header = f'<table width=100% style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" >' \
                    f'<tr>' \
                    f'<td width=20%  class="td_obroty" ><b>APTEKA</b></td>' \
                    f'<td width=20%  class="td_obroty"><b>PACJENCI</b></td>' \
                    f'<td width=20% class="td_obroty"><b>OBRÓT BRUTTO</b></td>' \
                    f'<td width=20% class="td_obroty"><b>OBRÓT NETTO</b></td>' \
                    f'<td width=20% class="td_obroty"><b>ZYSK NETTO</b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for d in dane:
        if d[4] != 'RAZEM':
            tabela_dane += f'<tr>' \
                           f'<td width=20%  class="td_obroty" ><b>{d[4]}</b></td>' \
                           f'<td width=20%  class="td_obroty" ><b>{d[0]}</b></td>' \
                           f'<td width=20%  class="td_obroty" ><b>{fp.currency_format(d[1])} zł</b></td>' \
                           f'<td width=20%  class="td_obroty" ><b>{fp.currency_format(d[2])} zł</b></td>' \
                           f'<td width=20%  class="td_obroty" ><b>{fp.currency_format(d[3])} zł</b></td>' \
                           '</tr>'
        else:
            tabela_dane += f'<tr style = "background-color: #c34f4f; font-size:14px;">' \
                           f'<td width=20%  class="td_obroty" ><b>{d[4]}</b></td>' \
                           f'<td width=20%  class="td_obroty" ><b>{d[0]}</b></td>' \
                           f'<td width=20%  class="td_obroty" ><b>{fp.currency_format(d[1])} zł</b></td>' \
                           f'<td width=20%  class="td_obroty" ><b>{fp.currency_format(d[2])} zł</b></td>' \
                           f'<td width=20%  class="td_obroty" ><b>{fp.currency_format(d[3])} zł</b></td>' \
                           '</tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie

    return tabela_koncowa


# TABELE I DANE DO STRONY GOTÓWKA #
def get_dane_gotowki(apteka):
    if apteka == '1':
        query = f'SELECT * FROM gotowki WHERE data > DATE_SUB(NOW(), INTERVAL 20 DAY) ORDER BY id_got DESC'
    else:
        query = f'SELECT * FROM gotowki WHERE data > DATE_SUB(NOW(), INTERVAL 180 DAY) AND ' \
                f'id_apteka = {apteka} ORDER BY id_got DESC'

    wynik = zpt_queries.zpt_query_fetchall(query)
    lista_z_color = []
    for d in wynik:
        color = '#ffffff'
        if d[2] == 9:
            color = '#db7f07'
        if d[2] != 9 and int(d[3]) < 0:
            color = '#b02007'


        lista_z_color.append(d + (color,))
    return lista_z_color

def tabela_gotowki(apteka):
    dane = get_dane_gotowki(apteka)
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=20%><b>DATA</b></td>' \
                    f'<td width=25%><b>MIEJSCE</b></td>' \
                    f'<td width=25%><b>KWOTA</b></td>' \
                    f'<td width=20%><b>OPIS</b></td>' \
                    f'<td width=10%><b></b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr class="tr_edit" style="color: {d[5]}">' \
                    f'<td width=20%>{d[1]}</td>' \
                    f'<td width=25% >{slowniki.gotowki_tabela[d[2]]}</td>' \
                    f'<td width=25%>{d[3]} zł</td>' \
                    f'<td width=20%>{d[4]}</td>' \
                       f'<td width=10%><button class="button_edit_icon" type="submit" name="gotowki_edycja_id" ' \
                       f'form="gotowki_edycja" value="{d[0]}">' \
                       f'<i class="bi bi-pencil-square"></i></button>&nbsp;&nbsp;' \
                       f'<button class="button_edit_icon" type="submit" name="gotowki_usun_id" ' \
                       f'form="gotowki_edycja" value="{d[0]}">' \
                       f'<i class="bi bi-trash"></i></button></td>' \
                       f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie

    return tabela_koncowa

# TABELE I DANE DO STRONY FAKTURY #

def get_dane_koszty_do_zaplaty():
    query =f'SELECT f.id_fv, k.nazwa, f.nr_fv, f.kwota, f.data_platnosci FROM ' \
             f'platnosci_kontrahenci k, platnosci_fv f WHERE ' \
             f'f.id_kont=k.id_kont AND f.zaplacone = 0 ORDER BY data_platnosci'
    wynik = zpt_queries.zpt_query_fetchall(query)
    lista = []
    for d in wynik:
        if check_date_deley(d[4]):
            color = '#ffffff'
        else:
            color = '#c34f4f'
        lista.append(d + (color,))
    return lista

def check_date_deley(date):
    date_1 = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_now = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
    if date_1 <= date_now:
        return False
    return True

def tabela_koszty_do_zaplaty():
    dane = get_dane_koszty_do_zaplaty()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=8% ><b></b></td>' \
                    f'<td width=37% ><b>KONTRAHENT</b></td>' \
                    f'<td width=15% ><b>FAKTURA</b></td>' \
                    f'<td width=15% ><b>KWOTA</b></td>' \
                    f'<td width=15% ><b>DATA PŁATNOŚCI</b></td>' \
                    f'<td width=10% ><b></b></td>' \
                    f'<tr>'
    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr class="tr_edit" style="color: {d[5]};">' \
                        f'{sprawdz_czy_faktura_w_buforze(d[0])}' \
                    f'</b></td>' \
                    f'<td width=37% ><b>{d[1]}</b></td>' \
                    f'<td width=15% ><b>{d[2]}</b></td>' \
                    f'<td width=15% ><b>{fp.currency_format(float(d[3]))} zł</b></td>' \
                    f'<td width=15% ><b>{d[4]}</b></td>' \
                    f'<td width=10% ><b>' \
                       f'<button class="button_edit_icon" type="submit" name="koszty_edycja_id" ' \
                       f'form="koszty_edycja" value="{d[0]}">' \
                       f'<i class="bi bi-pencil-square"></i></button>' \
                       f'&nbsp;&nbsp;' \
                       f'<button class="button_edit_icon" type="submit" name="id_koszty_usun" ' \
                       f'form="koszty_edycja" value="{d[0]}">' \
                       f'<i class="bi bi-trash"></i></button>' \
                       f'</td>' \
                    f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_koszty_kontrahenci():
    query = f'SELECT * FROM platnosci_kontrahenci ORDER BY nazwa'
    wynik = zpt_queries.zpt_query_fetchall(query)
    return wynik

def table_koszty_kontrahenci():
    dane = get_dane_koszty_kontrahenci()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=40% ><b>NAZWA</b></td>' \
                    f'<td width=20% ><b>NIP</b></td>' \
                    f'<td width=30% ><b>KONTO</b></td>' \
                    f'<td width=10% ><b></b></td>' \
                    f'<tr>'
    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr class="tr_edit">' \
                       f'<td width=40% ><b>{d[1]}</b></td>' \
                        f'<td width=20% ><b>{d[2]}</b></td>' \
                        f'<td width=30% ><b>{d[3]}</b></td>' \
                        f'<td width=10% >' \
                           f'<button class="button_edit_icon" type="submit" name="kontrahent_edytuj_id" ' \
                           f'form="kontrahent_edytuj" value="{d[0]}">' \
                           f'<i class="bi bi-pencil-square"></i></button>' \
                           f'&nbsp;&nbsp;' \
                           f'<button class="button_edit_icon" type="submit" name="id_koszty_kontrahent_usun" ' \
                           f'form="kontrahent_edytuj" value="{d[0]}">' \
                           f'<i class="bi bi-trash"></i></button>' \
                       f'</td>' \
                       f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_kontrahenci_faktury(id_kont):
    query = f'SELECT * FROM platnosci_fv WHERE id_kont = {id_kont} ORDER BY zaplacone, data_zaplaty DESC'
    wynik = zpt_queries.zpt_query_fetchall(query)
    return wynik

def tabele_koszty_kontrahenci_faktury(id_kont):
    dane = get_dane_kontrahenci_faktury(id_kont)
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=40% ><b>FAKTURA</b></td>' \
                    f'<td width=20% ><b>KWOTA</b></td>' \
                    f'<td width=20% ><b>TREMIN</b></td>' \
                    f'<td width=20% ><b>DATA ZAPŁATY</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr class="tr_edit" >' \
                    f'<td width=40% ><b>{d[2]}</b></td>' \
                    f'<td width=20% ><b>{d[3]}</b></td>' \
                    f'<td width=20% ><b>{d[4]}</b></td>' \
                    f'<td width=20% ><b>{d[5]}</b></td>' \
                       f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_towar_faktuty():
    query = f'SELECT apteka, nrfv, data_zak, data_platnosci, kwota, dost_nazwa ' \
                                     f'FROM platnosci_towar WHERE zaplacone = 0 ' \
                                     f' ORDER BY dost_nazwa, data_platnosci'
    wynik = zpt_queries.zpt_query_fetchall(query)

    wynik_dict = {}
    for n in wynik:
        if n[5] not in wynik_dict.keys():
            wynik_dict[f'{n[5]}'] = []
            wynik_dict[f'{n[5]}'].append(n)
        else:
            wynik_dict[f'{n[5]}'].append(n)
    return wynik_dict

def sprawdz_czy_faktura_w_buforze(faktura):
    query = f'SELECT * FROM przelewy_bankowe_bufor WHERE id_f = "{faktura}"'
    wynik = zpt_queries.zpt_query_fetchall(query)
    if len(wynik) == 0:
        form_text = f'<td width=8% ><b>' \
                    f'<input class="form-check-input" type="checkbox" name="checkbox_" value="{faktura}">'
    else:
        form_text = f'<td width=8%  style="color: green"><b>B'
    return form_text

def tabele_towar_faktury():
    dane = get_dane_towar_faktuty()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=5% ><b></b></td>' \
                    f'<td width=8% ><b>APTEKA</b></td>' \
                    f'<td width=25% ><b>FAKTURA</b></td>' \
                    f'<td width=20% ><b>DATA ZAKUPU</b></td>' \
                    f'<td width=20% ><b>TERMIN</b></td>' \
                    f'<td width=15% ><b>KWOTA</b></td>' \
                    f'<td width=7% ><b></b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for key in dane:
        razem = 0
        tabela_dane += f'<tr class="tr_towar_kontrahent">' \
                        f'<td colspan=7 ><b>{key}</b></td>' \
                        f'<tr>'
        for d in dane[f'{key}']:
            razem += d[4]
            # < input class ="form-check-input" type="checkbox" name="chceckbox_" value="{d[1]}" >
            tabela_dane += f'<tr class="tr_edit">' \
                        f'{sprawdz_czy_faktura_w_buforze(d[1])}' \
                    f'</b></td>' \
                    f'<td width=8% ><b>{d[0]}</b></td>' \
                    f'<td width=25% ><b>{d[1]}</b></td>' \
                    f'<td width=20% ><b>{d[2]}</b></td>' \
                    f'<td width=20% ><b>{d[3]}</b></td>' \
                    f'<td width=15% ><b>{fp.currency_format(d[4])} zł</b></td>' \
                    f'<td width=7% >' \
                   f'<button class="button_cash_icon" type="submit" name="towar_faktury_id"' \
                   f' form="towar_faktury" value="{d[1]}"><i class="bi bi-cash-stack"></i></button>' \
                   f'</td>' \
                    f'<tr>'
        tabela_dane += f'<tr>' \
                       f'<td class="td_towar_razem" colspan=5 ><b>RAZEM</b></td>' \
                       f'<td width=15% class="tr_edit"><b>{fp.currency_format(round(razem,2))} zł</b></td>' \
                       f'<td width=7%></td>' \
                       f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_towar_dostawcy():
    query = f'SELECT id, nazwa, nip, konto FROM dostawcy ORDER BY nazwa'
    wynik = zpt_queries.zpt_query_fetchall(query)
    return wynik

def tabela_towar_dostawcy():
    dane = get_dane_towar_dostawcy()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=35% ><b>NAZWA</b></td>' \
                    f'<td width=20% ><b>NIP</b></td>' \
                    f'<td width=35% ><b>KONTO</b></td>' \
                    f'<td width=10% ></td>' \
                    f'<tr>'
    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr class="tr_edit">' \
                       f'<td width=35% ><b>{d[1]}</b></td>' \
                        f'<td width=20% ><b>{d[2]}</b></td>' \
                        f'<td width=35% ><b>{d[3]}</b></td>' \
                       f'<td width=10% >' \
                           f'<button class="button_edit_icon" type="submit" name="dostawca_edytuj_id" ' \
                           f'form="dostawca_edycja" value="{d[0]}">' \
                           f'<i class="bi bi-pencil-square"></i></button>' \
                           f'&nbsp;&nbsp;' \
                           f'<button class="button_edit_icon" type="submit" name="id_towar_dostawcy_usun" ' \
                           f'form="dostawca_edycja" value="{d[0]}">' \
                           f'<i class="bi bi-trash"></i></button>' \
                       f'</td>' \
                       f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_towar_dostawcy_faktury(id_dostawcy):
    query = f'SELECT * FROM platnosci_towar WHERE dostawca = {id_dostawcy} ORDER BY data_platnosci DESC'
    wynik = zpt_queries.zpt_query_fetchall(query)
    return wynik

def tabela_towar_dostawcy_faktury(id_dostawcy):
    dane = get_dane_towar_dostawcy_faktury(id_dostawcy)
    if dane == ():
        return ''

    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=8%  ><b>APTEKA</b></td>' \
                    f'<td width=32%  ><b>FAKTURA</b></td>' \
                    f'<td width=15% ><b>DATA ZAKUPU</b></td>' \
                    f'<td width=15% ><b>TERMIN</b></td>' \
                    f'<td width=15% ><b>KWOTA</b></td>' \
                    f'<td width=15% ><b>DATA ZAPŁATY</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    for d in dane:
        if d[6] == 1:
            data_zaplaty = d[7]
        elif d[6] == 2:
            data_zaplaty = 'GOTÓWKA'
        elif d[6] == 0:
            data_zaplaty = ''

        tabela_dane += f'<tr class="tr_edit" >' \
                       f'<td width=8%  ><b>{d[0]}</b></td>' \
                    f'<td width=32%  ><b>{d[2]}</b></td>' \
                    f'<td width=15% ><b>{d[3]}</b></td>' \
                    f'<td width=15% ><b>{d[4]}</b></td>' \
                    f'<td width=15% ><b>{d[5]} zł</b></td>' \
                    f'<td width=15% ><b>{data_zaplaty}</b></td>' \
                       f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_tabela_faktury_wyszukaj(numer_faktury):
    faktury_znalezione = []
    for n in range(2,9):
        query = f'SELECT z.dat_zak_fv, d.nazwa, z.nrfv FROM zakupy_0{n} z, dostawcy d WHERE z.nrfv' \
                f' LIKE "{numer_faktury}%" AND z.dostawca = d.id_0{n}'
        wynik = zpt_queries.zpt_query_fetchall(query)

        for w in wynik:
            faktury_znalezione.append([n] + list(w))

    return faktury_znalezione

def tabela_faktury_wyszukaj(numer_faktury):
    dane = get_dane_tabela_faktury_wyszukaj(numer_faktury)
    tabela_header = f'<table width=80% style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse; color: white; font-size: 12px" class="table">' \
                    f'<tr>' \
                    f'<td width=20%><b>APTEKA</b></td>' \
                    f'<td width=30%><b>FAKTURA</b></td>' \
                    f'<td width=25%><b>DATA ZAKUPU</b></td>' \
                    f'<td width=25%><b>DOSTAWCA</b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr>' \
                    f'<td width=20%>{slowniki.gotowki_tabela[d[0]]}</td>' \
                    f'<td width=30%>{d[3]}</td>' \
                    f'<td width=25%>{d[1][0:10]}</td>' \
                    f'<td width=25%>{d[2]}</td>' \
                    f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

# TABELE I DANE DO STRONY PRZELEWY #

def get_dane_przelewy_wykaz():
    query = f'SELECT * FROM przelewy_bankowe ORDER BY data DESC LIMIT 250'
    wynik = zpt_queries.zpt_query_fetchall(query)
    return wynik

def tabela_przelewy_wykaz():
    dane = get_dane_przelewy_wykaz()
    tabela_header = f'<table width=80% style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=25% ><b>KONTRAHENT</b></td>' \
                    f'<td width=15% ><b>DATA</b></td>' \
                    f'<td width=15%><b>KWOTA</b></td>' \
                    f'<td width=45%><b>TYTUŁ</b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr class="tr_edit" >' \
                       f'<td width=25% >{d[1]}</td>' \
                        f'<td width=15% >{d[2]}</td>' \
                        f'<td width=15%>{fp.currency_format(float(d[3]))} zł</td>' \
                        f'<td width=45%>{d[4]}</td>' \
                       f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_tabela_bufor():
    query = f'SELECT * FROM przelewy_bankowe_bufor'
    wynik = zpt_queries.zpt_query_fetchall(query)
    bufor_dict = {}

    wynik_dict = {}
    for n in wynik:
        if n[3] not in wynik_dict.keys():
            wynik_dict[f'{n[3]}'] = []
            wynik_dict[f'{n[3]}'].append(n)
        else:
            wynik_dict[f'{n[3]}'].append(n)
    return wynik_dict

def tabela_przelewy_bufor():
    dane = get_dane_tabela_bufor()
    saldo = 0
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=15% ><b>RODZAJ</b></td>' \
                    f'<td width=40% ><b>FAKTURA</b></td>' \
                    f'<td width=30% ><b>KWOTA</b></td>' \
                    f'<td width=15% ><b></b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for key in dane:
        razem = 0
        tabela_dane += f'<tr>' \
                       f'<td class="tr_towar_kontrahent" colspan=4 ><b>{key}</b></td>'
        for d in dane[f'{key}']:
            razem += float(d[5])
            if d[1] == 'T':
                rodzaj = 'TOWAR'
                color = ''
            elif d[1] == 'K':
                rodzaj = 'KOSZTY'
                color = ''
            elif d[1] == 'H':
                rodzaj = 'HURTOWNIA'
                color = ''
            saldo += float(d[5])
            tabela_dane += f'<tr class="tr_edit">'\
                           f'<td width=15% ><b>{rodzaj}</b></td>' \
                           f'<td width=40% ><b>{d[7]}</b></td>' \
                           f'<td width=30% ><b>{d[5]} zł</b></td>' \
                           f'<td width=15% >' \
                           f'<button class="button_icon" type="submit" name="delete_bufor_id"' \
                           f' form="delete_bufor" value="{d[0]}"><i class="bi bi-trash"></i></button>' \
                           f'</td>' \
                           f'<tr>'
        tabela_dane += f'<tr>' \
                       f'<td class="td_towar_razem" colspan=3 ><b>RAZEM</b></td>' \
                       f'<td class="tr_edit"><b>{fp.currency_format(round(razem, 2))} zł</b></td>' \
                       f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa, saldo

def get_dane_przelewy_szukaj(fraza, szukaj_w):
    if szukaj_w == 'tytul':
        query = f'SELECT * FROM przelewy_bankowe WHERE tytul LIKE "%{fraza}%" ORDER BY data DESC LIMIT 250'
    elif szukaj_w == 'odbiorca':
        query = f'SELECT * FROM przelewy_bankowe WHERE kontrahent LIKE "%{fraza}%" ORDER BY data DESC LIMIT 250'
    else:
        return ''
    wynik = zpt_queries.zpt_query_fetchall(query)
    return wynik

def tabela_przelewy_szukaj(fraza, szukaj_w):
    dane = get_dane_przelewy_szukaj(fraza, szukaj_w)
    if dane == '':
        return ''
    else:
        tabela_header = f'<table width=80% style = "margin-left: auto; margin-right: auto; text-align: center;' \
                        f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                        f'<tr class="tr_header">' \
                        f'<td width=35%><b>KONTRAHENT</b></td>' \
                        f'<td width=15%><b>DATA</b></td>' \
                        f'<td width=25%><b>KWOTA</b></td>' \
                        f'<td width=25%><b>TYTUŁ</b></td>' \
                        f'<tr>'
        tabela_dane = ''
        for d in dane:
            tabela_dane += f'<tr class="tr_edit">' \
                           f'<td width=35%>{d[1]}</td>' \
                           f'<td width=15%>{d[2]}</td>' \
                           f'<td width=25%>{fp.currency_format(float(d[3]))} zł</td>' \
                           f'<td width=25%>{d[4]}</td>' \
                           f'<tr>'

        tabela_zakonczenie = '</table>'
        tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
        return tabela_koncowa


# TABELE HURTOWNIE
def get_dane_hurtownie_faktury(hurtownia):
    query = f'SELECT dane_json FROM hurtownie_do_zaplaty WHERE hurtownia= "{hurtownia}"'
    wynik = zpt_queries.zpt_query_fetchone(query)
    if wynik == None:
        return []
    wynik_lista = json.loads(wynik[0])

    return wynik_lista

def tabela_hurtownie_fv(dane, data):
    if dane == []:
        return ('', 'BRAK DANYCH W BAZIE DANCYCH')
    saldo = 0

    tabela_header = f'<table width=80% style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" >' \
                    f'<tr class="keeptogether">' \
                    f'<td width=25%  class="td_obroty"><b>FAKTURA</b></td>' \
                    f'<td width=25%  class="td_obroty"><b>DATA PŁATNOŚCI</b></td>' \
                    f'<td width=25% class="td_obroty"><b>DATA ZAKUPU</b></td>' \
                    f'<td width=25% class="td_obroty"><b>KWOTA</b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for d in dane:
        if data == str(datetime.datetime.now().date()):
            saldo += float(d[4])
            tabela_dane += f'<tr class="keeptogether" >' \
                           f'<td width=25%  class="td_obroty"><b>{d[1]}</b></td>' \
                           f'<td width=25%  class="td_obroty"><b>{d[2]}</b></td>' \
                           f'<td width=25% class="td_obroty"><b>{d[3]}</b></td>' \
                           f'<td width=25% class="td_obroty"><b>{fp.currency_format(float(d[4]))} zł</b></td>' \
                           f'<tr>'
        else:
            if d[2] <= data:
                saldo += float(d[4])
                tabela_dane += f'<tr class="keeptogether" >' \
                               f'<td width=25%  class="td_obroty"><b>{d[1]}</b></td>' \
                            f'<td width=25%  class="td_obroty"><b>{d[2]}</b></td>' \
                            f'<td width=25% class="td_obroty"><b>{d[3]}</b></td>' \
                            f'<td width=25% class="td_obroty"><b>{fp.currency_format(float(d[4]))} zł</b></td>' \
                               f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return (tabela_koncowa, f'{saldo:0.2f}')

def tabela_hurtownie_zestawienie_eksport_do_pliku(hurtownia, dane, data):
    config = pdfkit.configuration(wkhtmltopdf='c:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    saldo = 0
    dane_tabela_zestawienie = []
    for d in dane:
        if d[2] <= data:
            saldo += float(d[4])
            dane_tabela_zestawienie.append(d)

    tabela_text = f'<table border="1" cellspacing="0" cellpadding="4" style="text-align: center; width:100%;">' \
                    f'<tr>' \
                    f'<td width=10% "><b>Nr kontr.</b></td>' \
                    f'<td width=30%  "><b>Nr dokumentu</b></td>' \
                    f'<td width=15% "><b>Data płatności</b></td>' \
                    f'<td width=15% "><b>Data wystawienia</b></td>' \
                    f'<td width=15% "><b>Wartość brutto</b></td>' \
                    f'<td width=15% "><b>Do zapłaty</b></td>' \
                    f'<tr>'

    for d in dane_tabela_zestawienie:
        tabela_text += f'<tr>' \
                    f'<td width=10% ">{d[0]}</td>' \
                    f'<td width=30%  ">{d[1]}</td>' \
                    f'<td width=15% ">{d[2]}</td>' \
                    f'<td width=15% ">{d[3]}</td>' \
                    f'<td width=15% ">{d[4]}</td>' \
                    f'<td width=15% ">{d[5]}</td>' \
                    f'<tr>'

    tabela_text += f'<tr>' \
                          f'<td colspan="4"><b>RAZEM &emsp;&emsp;&emsp;</b></td>' \
                          f'<td colspan="2"><b>{saldo:0.2f} zł</b></td>' \
                          f'</tr></table>'


    with open(staticfiles_storage.path('szablony/hurtownie_zestawienie.html'), "r", encoding='utf-8') as f:
        text = f.read()

    data_generacji = str(datetime.date.today()).replace('-', '')
    if hurtownia == "NEUCA":
        nazwa_pliku = f'129551_NEUCA_{data_generacji}_{saldo:0.2f}'
    else:
        nazwa_pliku = f'5472110371_{hurtownia}_{data_generacji}_{saldo:0.2f}'

    text = text.replace('__nazwa_pliku__', f'{nazwa_pliku}')
    text = text.replace('__tabela_z_danymi__',f'{tabela_text}')

    pdf_path = rf'C:\Users\dell\Desktop\{nazwa_pliku}.pdf'
    pdfkit.from_string(text, pdf_path, configuration=config)

    return f'Zapisano plik zestawienia: {pdf_path}'

def get_dane_hurtownie_zestawienia(hurtownia):
    if hurtownia != '':
        query = f'SELECT * FROM hurtownie_zestawienia WHERE hurtownia = "{hurtownia}" ORDER By data DESC'
    else:
        query = f'SELECT * FROM hurtownie_zestawienia ORDER By data DESC'
    wynik = zpt_queries.zpt_query_fetchall(query)
    return wynik

def tabela_hurtownie_zestawienia(hurtownia=''):
    dane = get_dane_hurtownie_zestawienia(hurtownia)
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=30% ><b>HURTOWNIA</b></td>' \
                    f'<td width=30% ><b>DATA PŁATNOŚCI</b></td>' \
                    f'<td width=30% ><b>SUMA PRZELEWU</b></td>' \
                    f'<td width=10% ><b> </b></td>' \
                    f'<tr>'

    tabela_dane = ''

    for d in dane:
        saldo = 0
        for fv in json.loads(d[3]):
            saldo += float(fv[4])
        # f'<tr  class="tr_edit" onclick="location.href=\'hurtownie_zestawienia?id={d[0]}\'">'
        tabela_dane += f'<tr  class="tr_edit">' \
                       f'<td width=30% >{d[1]}</td>' \
                        f'<td width=30% >{d[2]}</td>' \
                     f'<td width=30% >{fp.currency_format(saldo)} zł</td>' \
                     f'<td width=10% >' \
                       f'<button class="button_edit_icon" type="submit" name="hurtownie_zestawienia_szczegoly_id" ' \
                       f'form="hurtownie_zestawienia_szcegoly" value="{d[0]}">' \
                       f'<i class="bi bi-search"></i></button>' \
                       f'&nbsp;&nbsp;' \
                       f'<button class="button_edit_icon" type="submit" name="hurtownie_zestawienia_rozlicz_id" ' \
                       f'form="hurtownie_zestawienia_szcegoly" value="{d[0]}">' \
                       f'<i class="bi bi-calculator"></i></button>' \
                       f'</td>' \
                       f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_hurtownie_zestawienia_szcegoly(id_zestawienia):
    query = f'SELECT * FROM hurtownie_zestawienia WHERE id_zestawienia = "{id_zestawienia}"'
    wynik = zpt_queries.zpt_query_fetchone(query)
    return wynik

def tabela_hurtownie_zestawienia_szczegoly(id_zestawienie):
    dane = get_dane_hurtownie_zestawienia_szcegoly(id_zestawienie)
    dane_do_zwrotu = {}
    dane_do_zwrotu['hurtownia'] = dane[1]
    dane_do_zwrotu['data'] = dane[2]

    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=5% ><b>LP.</b></td>' \
                    f'<td width=30% ><b>FAKTURA</b></td>' \
                    f'<td width=20% ><b>TERMIN PŁATNOŚCI</b></td>' \
                    f'<td width=20% ><b>DATA WYSTAWIENIA</b></td>' \
                    f'<td width=25% ><b>KWOTA</b></td>' \
                    f'<tr>'

    tabela_dane = ''

    n = 1
    saldo = 0
    for d in json.loads(dane[3]):
        saldo += float(d[4])
        tabela_dane += f'<tr  class="tr_edit">' \
                       f'<td width=5% ><b>{n}</b></td>' \
                        f'<td width=30% ><b>{d[1]}</b></td>' \
                        f'<td width=20% ><b>{d[2]}</b></td>' \
                        f'<td width=20% ><b>{d[3]}</b></td>' \
                        f'<td width=25% ><b>{d[4]}</b></td>' \
                       f'<tr>'
        n+=1
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    dane_do_zwrotu['saldo'] = fp.currency_format(saldo)
    dane_do_zwrotu['tabela'] = tabela_koncowa
    return dane_do_zwrotu

def get_dane_tabela_hurtownie_poziom_zakupow(miesiac):
    query = f'SELECT * FROM zakupy_hurtownie WHERE miesiac = "{miesiac}"'
    wynik = zpt_queries.zpt_query_fetchall(query)

    wynik_lista = []
    #zmiana wynik na listy
    for w in wynik:
        wynik_lista.append(list(w))
    wynik_lista.sort(key=lambda x: x[1])

    return wynik_lista

def tabela_hurtownie_poziom_zakupow(miesiac):
    dane = get_dane_tabela_hurtownie_poziom_zakupow(miesiac)
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=25%><b>APTEKA</b></td>' \
                    f'<td width=25%><b>ZAKUPY HURTOWNIE</b></td>' \
                    f'<td width=25%><b>ZAKUPY NEUCA</b></td>' \
                    f'<td width=25%><b>POZIOM ZAKUPÓW</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    for apteka in dane:
        apteka_nazwa = slowniki.online_id_nazwa[f'{apteka[1]}']
        suma_hurtownie_zakupy_kwoty = sum(json.loads(apteka[4]).values())
        zakupy_kwoty_neuca = json.loads(apteka[4])['NEUCA']
        zakupy_procent_neuca = json.loads(apteka[5])['NEUCA']

        alert_color = ''
        if zakupy_procent_neuca < 80:
            alert_color = 'style="color: red;"'

        tabela_dane += f'<tr class="tr_header" {alert_color}>' \
                    f'<td width=25%>{apteka_nazwa}</td>' \
                    f'<td width=25%>{fp.currency_format(suma_hurtownie_zakupy_kwoty)} zł</td>' \
                    f'<td width=25%>{fp.currency_format(zakupy_kwoty_neuca)} zł</td>' \
                    f'<td width=25%>{zakupy_procent_neuca} %</td>' \
                    f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_hurtownie_wyslij_zestawinie():
    dane = fp.get_dane_hurtownie_maile_wyslij_zestawienia()
    if dane == []:
        return ''

    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=20% ><b>HURTOWNIA</b></td>' \
                    f'<td width=55% ><b>PLIK</b></td>' \
                    f'<td width=25% ><b>EMAIL</b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr  class="tr_edit">' \
                        f'<td width=20% >{d["hurtownia"]}</td>' \
                        f'<td width=55% >{d["plik"]}</td>' \
                        f'<td width=25% >{d["email"]}</td>' \
                        f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa


# TABELE PRACOWNICY

def get_dane_pracownicy_dane(id_pracownika):
    if id_pracownika != '0':
        with open(staticfiles_storage.path('json/pracownicy.json'), "r", encoding='utf-8') as json_file:
            dane = json.load(json_file)
    else:
        return []
    return dane[id_pracownika]

def tabela_pracownicy_dane(id_pracownika):
    dane = get_dane_pracownicy_dane(id_pracownika)
    if dane == []:
        return ''
    color_aktywny = 'style="color: green"'
    if dane['aktywny'] != 'TAK':
        color_aktywny = 'style="color: red"'

    urlop = fp.get_ilosc_urlopu(id_pracownika)

    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header" {color_aktywny}>' \
                    f'<td  colspan=2><b>{dane["pelna_nazwa"]}</b></td>' \
                    f'<tr>'\
                    f'<tr class="tr_header">' \
                    f'<td  width=50%><b>STANOWISKO</b></td>' \
                    f'<td  width=50%>{dane["stanowisko"]}</td>' \
                    f'<tr>'\
    f'<tr class="tr_header">' \
    f'<td  width=50%><b>PLACÓWKA</b></td>' \
    f'<td  width=50%>{dane["placowka"]}</td>' \
    f'<tr>'\
    f'<tr class="tr_header">' \
    f'<td  width=50%><b>POZOSTAŁY URLOP</b></td>' \
    f'<td  width=50%>{urlop}</td>' \
    f'<tr>'\
    f'<tr class="tr_header">' \
    f'<td  width=50%><b>PENSJA (BRUTTO)</b></td>' \
    f'<td  width=50%>{dane["pensja"]}</td>' \
    f'<tr>'\
    f'<tr class="tr_header">' \
    f'<td  width=50%><b>BADANIA LEKARSKIE</b></td>' \
    f'<td  width=50%>{dane["badania"]}</td>' \
    f'<tr>'\
    f'<tr class="tr_header">' \
    f'<td  width=50%><b>KONIEC UMOWY</b></td>' \
    f'<td  width=50%>{dane["badania"]}</td>' \
    f'<tr>'\
    f'<tr class="tr_header">' \
    f'<td  width=50%><b>DATA URODZENIA</b></td>' \
    f'<td  width=50%>{dane["data_urodzenia"]}</td>' \
    f'<tr>' \
    f'<tr class="tr_header">' \
    f'<td  width=50%><b>UWAGI DO WYPŁATY</b></td>' \
    f'<td  width=50%>{dane["uwagi_wynagrodzenia"]}</td>' \
    f'<tr>' \
    f'<tr class="tr_header">' \
    f'<td  width=50%><b>PREMIA</b></td>' \
    f'<td  width=50%>{dane["premia"]}</td>' \
    f'<tr>'
    tabela_dane = ''
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_pracownicy_urlopy(id_pracownika):
    query = f'SELECT dane_json FROM pracownicy_nieobecnosci WHERE id_pracownika = {id_pracownika}'
    wynik = json.loads(zpt_queries.zpt_query_fetchone(query)[0])
    return wynik

def tabela_pracowniy_urlopy(dane):
    kolumny = fp.ustaw_kolumny_pracownicy_urlopy()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=10%><b>DNI</b></td>' \
                    f'<td width=22.5%><b>{kolumny[0]}</b></td>' \
                    f'<td width=22.5%><b>{kolumny[1]}</b></td>' \
                    f'<td width=22.5%><b>{kolumny[2]}</b></td>' \
                    f'<td width=22.5%><b>{kolumny[3]}</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    for n in range(26):
        dane_do_wpisania = []
        for rok in kolumny:

            if str(rok) in list(dane['urlopy'].keys()):
                lista_urlopow = dane['urlopy'][f'{rok}']
                lista_urlopow.sort()

                if n >= len(dane['urlopy'][f'{rok}']):
                    dane_do_wpisania.append('')
                else:
                    dane_do_wpisania.append(lista_urlopow[n])
            else:
                dane_do_wpisania.append('')
        tabela_dane += f'<tr class="tr_edit">' \
                    f'<td width=10%><b>{n+1}</b></td>' \
                    f'<td width=22.5%>{dane_do_wpisania[0]}</td>' \
                    f'<td width=22.5%>{dane_do_wpisania[1]}</td>' \
                    f'<td width=22.5%>{dane_do_wpisania[2]}</td>' \
                    f'<td width=22.5%>{dane_do_wpisania[3]}</td>' \
                    f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_pracownicy_nieobecnosci_L4(dane):
    if dane == []:
        return ''
    dane.sort(key=lambda x: x[0])
    dane.reverse()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=10%><b>LP</b></td>' \
                    f'<td width=25%><b>DATA</b></td>' \
                    f'<td width=65%><b>UWAGI</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    n = 1
    for d in dane:
        tabela_dane += f'<tr class="tr_edit">' \
                    f'<td width=10%><b>{n}</b></td>' \
                    f'<td width=25%><b>{d[0]}</b></td>' \
                    f'<td width=65%><b>{d[1]}</b></td>' \
                    f'<tr>'
        n+=1

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_pracownicy_nieobecnosci_opieka_choroba(dane):
    if dane == []:
        return ''
    dane.sort(key=lambda x: x[0])
    dane.reverse()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=10%><b>LP</b></td>' \
                    f'<td width=25%><b>DATA</b></td>' \
                    f'<td width=65%><b>UWAGI</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    n = 1
    for d in dane:
        tabela_dane += f'<tr class="tr_edit">' \
                    f'<td width=10%><b>{n}</b></td>' \
                    f'<td width=25%><b>{d[0]}</b></td>' \
                    f'<td width=65%><b>{d[1]}</b></td>' \
                    f'<tr>'
        n+=1

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_pracownicy_nieobecnosci_opieka_zdrowe_dziecko(dane):
    if dane == []:
        return ''
    dane.sort(key=lambda x: x[0])
    dane.reverse()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=10%><b>LP</b></td>' \
                    f'<td width=25%><b>DATA</b></td>' \
                    f'<td width=65%><b>UWAGI</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    n = 1
    for d in dane:
        tabela_dane += f'<tr class="tr_edit">' \
                    f'<td width=10%><b>{n}</b></td>' \
                    f'<td width=25%><b>{d[0]}</b></td>' \
                    f'<td width=65%><b>{d[1]}</b></td>' \
                    f'<tr>'
        n+=1

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_pracownicy_nieobecnosci_urlop_okolicznosciowy(dane):
    if dane == []:
        return ''
    dane.sort(key=lambda x: x[0])
    dane.reverse()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=10%><b>LP</b></td>' \
                    f'<td width=25%><b>DATA</b></td>' \
                    f'<td width=65%><b>UWAGI</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    n = 1
    for d in dane:
        tabela_dane += f'<tr class="tr_edit">' \
                    f'<td width=10%><b>{n}</b></td>' \
                    f'<td width=25%><b>{d[0]}</b></td>' \
                    f'<td width=65%><b>{d[1]}</b></td>' \
                    f'<tr>'
        n+=1

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_pracownicy_nieobecnosci_wolne_za_swieto(dane):
    if dane == []:
        return ''
    dane.sort(key=lambda x: x[0])
    dane.reverse()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=10%><b>LP</b></td>' \
                    f'<td width=25%><b>DATA</b></td>' \
                    f'<td width=65%><b>UWAGI</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    n = 1
    for d in dane:
        tabela_dane += f'<tr class="tr_edit">' \
                    f'<td width=10%><b>{n}</b></td>' \
                    f'<td width=25%><b>{d[0]}</b></td>' \
                    f'<td width=65%><b>{d[1]}</b></td>' \
                    f'<tr>'
        n+=1

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa


#TABELE RÓŻNE
def get_dane_fundusze_l():
    query = f'SELECT * FROM gotowki_xx WHERE data > DATE_SUB(NOW(), INTERVAL 300 DAY) ORDER BY id DESC'
    wynik = zpt_queries.zpt_query_fetchall(query)

    lista_z_color = []
    for d in wynik:
        color = '#ffffff'
        if int(d[3]) < 0:
            color = '#b02007'

        lista_z_color.append(d + (color,))

    return lista_z_color

def tabela_fundusze_l():
    dane = get_dane_fundusze_l()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=20%><b>DATA</b></td>' \
                    f'<td width=30%><b>KWOTA</b></td>' \
                    f'<td width=40%><b>OPIS</b></td>' \
                    f'<td width=10%></td>' \
                    f'<tr>'
    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr class="tr_edit" style="color: {d[4]}">' \
                        f'<td width=20%>{d[1]}</td>' \
                        f'<td width=30%>{d[3]}</td>' \
                        f'<td width=40%>{d[2]}</td>' \
                        f'<td width=10%><button class="button_edit_icon" type="submit" name="fundusze_l_edycja_id" ' \
                       f'form="fundusze_l_edycja" value="{d[0]}">' \
                       f'<i class="bi bi-pencil-square"></i></button>&nbsp;&nbsp;' \
                       f'<button class="button_edit_icon" type="submit" name="fundusze_l_usun_id" ' \
                       f'form="fundusze_l_edycja" value="{d[0]}">' \
                       f'<i class="bi bi-trash"></i></button></td>' \
                        f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_karty_hallera():
    with open(staticfiles_storage.path('json/karty_hallera.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)


    lista_dat = sorted(list(dane.keys()))
    lista_dat.reverse()
    if len(lista_dat) > 40:
        lista_dat = lista_dat[:40]

    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=20%><b>DATA</b></td>' \
                    f'<td width=30%><b>KWOTA KAMSOFT</b></td>' \
                    f'<td width=40%><b>KWOTA TERMINAL</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    for d in lista_dat:
        if dane[d]['rozliczone'] == 0:
            color = 'red'
        else:
            color = 'green'

        tabela_dane += f'<tr class="tr_edit" style="color: {color}">' \
                       f'<td width=20%>{d}</td>' \
                       f'<td width=40%>{dane[d]["kwota_kamsoft"]}</td>' \
                       f'<td width=40%>{dane[d]["kwota_terminal"]}</td>' \
                       f'<tr>'
        if dane[d]['rozliczone'] == 1 or dane[d]["kwota_terminal"] == 0:
            continue
        else:
            roznice = fp.karty_hallera_znajdz_braki(d, round(dane[d]["kwota_terminal"] - dane[d]["kwota_kamsoft"],2))
            tabela_dane += f'<tr class="tr_edit">' \
                           f'<td colspan=3>{roznice}</td>' \
                           f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_czynsze():
    id_rachunek = 0
    with open(staticfiles_storage.path('json/czynsze.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    lista_slownikow = []
    for key in dane.keys():
        lista_slownikow.append(dane[key])
    lista_slownikow.sort(key=lambda x: x['data'])
    lista_slownikow.reverse()

    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=20%><b>NR RACHUNKU</b></td>' \
                    f'<td width=15%><b>DATA</b></td>' \
                    f'<td width=30%><b>NAJEMCA</b></td>' \
                    f'<td width=15%><b>KWOTA</b></td>' \
                    f'<td width=20%></td>' \
                    f'<tr>'
    tabela_dane = ''
    for k in lista_slownikow:
        # znajdowanie klucza po wartosci nr rachunku
        for key in dane:
            if dane[key]['nr'] == k['nr']:
                id_rachunek = key
                break

        #sprawdzenie wysłania mailem
        if k['mail'] == 1:
            mail = '<button class="button_edit_icon" type="submit" name="" ' \
                       f'form="czynsze_form_id" value="" style="color: green;">' \
                       f'<i class="bi bi-file-earmark-check"></i></button>'
        else:
            mail = '<button class="button_edit_icon" type="submit" name="czynsze_do_wyslania_mailem_id" ' \
                       f'form="czynsze_form_id" value="{id_rachunek}">' \
                       f'<i class="bi bi-file-earmark-arrow-up"></i></button>'

        tabela_dane += f'<tr class="tr_edit">' \
                    f'<td width=20%>{k["nr"]}</td>' \
                    f'<td width=15%>{k["data"]}</td>' \
                    f'<td width=30%>{k["najemca"]}</td>' \
                    f'<td width=15%>{k["suma"]}</td>' \
                    f'<td width=20%>{mail}' \
                       f'&nbsp;&nbsp;' \
                       f'<button class="button_edit_icon" type="submit" name="czynsze_do_skopiowania_id" ' \
                       f'form="czynsze_form_id" value="{id_rachunek}">' \
                       f'<i class="bi bi-files"></i></button>' \
                       f'&nbsp;&nbsp;' \
                       f'<button class="button_edit_icon" type="submit" name="czynsze_do_edycji_id" ' \
                       f'form="czynsze_form_id" value="{id_rachunek}">' \
                       f'<i class="bi bi-pencil-square"></i></button>' \
                       f'&nbsp;&nbsp;' \
                       f'<button class="button_edit_icon" type="submit" name="pdf_id" ' \
                       f'form="czynsze_form_id" value="{id_rachunek}">' \
                       f'<i class="bi bi-file-earmark-break"></i></button>' \
                       f'</td>' \
                    f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_tabela_biala_lista(nazwa_szukana):
    if nazwa_szukana == '':
        query = f'SELECT * FROM biala_lista ORDER BY id DESC LIMIT 200'
    else:
        query = f'SELECT * FROM biala_lista WHERE nazwa LIKE "%{nazwa_szukana}%" ORDER BY id DESC'
    wynik = zpt_queries.zpt_query_fetchall(query)
    return wynik

def tabela_biala_lista(nazwa_szukana):
    dane = get_dane_tabela_biala_lista(nazwa_szukana)
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=15%><b>DATA</b></td>' \
                    f'<td width=30%><b>NAZWA</b></td>' \
                    f'<td width=20%><b>KONTO</b></td>' \
                    f'<td width=10%><b>NIP</b></td>' \
                    f'<td width=10%><b>STATUS</b></td>' \
                    f'<td width=15%><b>KOD AUTORYZACJI</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr class="tr_edit">' \
                       f'<td width=15%>{d[1][:10]}</td>' \
                    f'<td width=30%>{d[2]}</td>' \
                    f'<td width=20%>{d[3]}</td>' \
                    f'<td width=10%>{d[4]}</td>' \
                    f'<td width=10%>{d[5]}</td>' \
                    f'<td width=15%>{d[6]}</td>' \
                    f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_dyzury(lista_dat):
    with open(staticfiles_storage.path('json/dyzury.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=20%><b>DATA</b></td>' \
                    f'<td width=30%><b>APTEKA</b></td>' \
                    f'<td width=35%><b>ADRES</b></td>' \
                    f'<td width=15%><b>TELEFON</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    for d in lista_dat:
        if dane[d]['apteka'] == 'Apteka Na Hallera ':
            color = 'style="color: red;"'
        else:
            color = ''
        tabela_dane += f'<tr class="tr_edit" {color}>' \
                       f'<td width=20%>{d}</td>' \
                    f'<td width=30%>{dane[d]["apteka"]}</td>' \
                    f'<td width=35%><b>{dane[d]["adres_1"]} {dane[d]["adres_2"]}</b></td>' \
                    f'<td width=15%>{dane[d]["telefon"]}</td>' \
                       f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_reklamowki(apteka, lista_miesiecy):
    lista_sprzedaz_kwartal = []
    for d in lista_miesiecy:
        query = f'SELECT SUM(ilosp) FROM sprzedaz_0{apteka} WHERE idtowr = {slowniki.reklamowki_id_towaru[apteka]} ' \
                               f'AND datsp LIKE "%{d}%"'
        wynik = zpt_queries.zpt_query_fetchone(query)[0]
        lista_sprzedaz_kwartal.append(wynik)
    return lista_sprzedaz_kwartal

def tabela_reklamowki_raport(kwartal, rok):
    lista_miesiecy = []
    for m in slowniki.rozne_reklamowiki_kwartal_dict[kwartal]:
        lista_miesiecy.append(f'{rok}-{m}')

    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=25% ><b>APTEKA</b></td>' \
                    f'<td width=25% ><b>{lista_miesiecy[0]}</b></td>' \
                    f'<td width=25% ><b>{lista_miesiecy[1]}</b></td>' \
                    f'<td width=25% ><b>{lista_miesiecy[2]}</b></td>' \
                    f'<tr>'

    tabela_dane = ''

    for apteka in range(2,9):
        if apteka == 3:
            continue
        dane_sprzedaz = get_dane_reklamowki(f'{apteka}', lista_miesiecy)
        apteka_nazwa = slowniki.online_id_nazwa[f'{apteka}']
        tabela_dane += f'<tr  class="tr_edit">' \
                       f'<td width=25% ><b>{apteka_nazwa}</b></td>' \
                       f'<td width=25% >{dane_sprzedaz[0]}</td>' \
                       f'<td width=25% >{dane_sprzedaz[1]}</td>' \
                       f'<td width=25% >{dane_sprzedaz[2]}</td>' \
                       f'<tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_tabela_todo_list():
    with open(staticfiles_storage.path('json/todo.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    lista_todo = []
    for d in dane:
        if dane[d]['status'] == '0':
            lista_todo.append([d, dane[d]['termin'], dane[d]['nazwa'], dane[d]['data_dodania']])
    lista_todo.sort(key=lambda x: x[1])
    return lista_todo

def tabela_todo_list():
    dane = get_dane_tabela_todo_list()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=7% ><b>LP</b></td>' \
                    f'<td width=20% ><b>TERMIN</b></td>' \
                    f'<td width=43% ><b>NAZWA</b></td>' \
                    f'<td width=20% ><b>DATA DODANIA</b></td>' \
                    f'<td width=10% ><b></b></td>' \
                    f'<tr>'

    tabela_dane = ''
    n = 1
    # document.getElementById("myForm").submit();
    for d in dane:
        tabela_dane += f'<tr  class="tr_edit">' \
                       f'<td width=7% >{n}</td>' \
                        f'<td width=20% >{d[1]}</td>' \
                        f'<td width=43% >{d[2]}</td>' \
                        f'<td width=20% >{d[3]}</td>' \
                        f'<td width=10% >' \
                       f'<button class="button_edit_icon" type="submit" name="todo_edit_id" ' \
                       f'form="todo_edit" value="{d[0]}">' \
                       f'<i class="bi bi-pencil-square"></i></button>' \
                       f'&nbsp;&nbsp;' \
                       f'<button class="button_edit_icon" type="submit" name="todo_delete_id" ' \
                       f'form="todo_edit" value="{d[0]}">' \
                       f'<i class="bi bi-trash"></i></button>' \
                       f'</td>' \
                       f'<tr>'
        n += 1
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_tabela_todo_list_done():
    with open(staticfiles_storage.path('json/todo.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    lista_done = []
    for d in dane:
        if dane[d]['status'] == '1':
            lista_done.append([d, dane[d]['termin'], dane[d]['nazwa'], dane[d]['data_zamkniecia']])
    lista_done.sort(key=lambda x: x[3])
    lista_done.reverse()
    return lista_done

def tabela_todo_list_done():
    dane = get_dane_tabela_todo_list_done()
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=7% ><b>LP</b></td>' \
                    f'<td width=20% ><b>TERMIN</b></td>' \
                    f'<td width=43% ><b>NAZWA</b></td>' \
                    f'<td width=20% ><b>DATA ZAKOŃCZENIA</b></td>' \
                    f'<td width=10% ><b></b></td>' \
                    f'<tr>'

    tabela_dane = ''
    n = 1
    for d in dane:
        tabela_dane += f'<tr  class="tr_edit">' \
                       f'<td width=7% >{n}</td>' \
                       f'<td width=20% >{d[1]}</td>' \
                       f'<td width=43% >{d[2]}</td>' \
                       f'<td width=20% >{d[3]}</td>' \
                       f'<td width=10% >' \
                       f'<button class="button_edit_icon" type="submit" name="done_edit_id" ' \
                       f'form="done_edit" value="{d[0]}">' \
                       f'<i class="bi bi-pencil-square"></i></button>' \
                       f'</td>' \
                       f'<tr>'
        n += 1
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def get_dane_archiwa(data_od, data_do):
    obroty_archiwa_dict = {}
    all_pacjenci = 0
    all_brutto = 0
    all_netto = 0
    all_zysk = 0

    for n in range(2, 9):
        if n == 3:
            continue
        guerry_obroty_archiwa = f'SELECT SUM(pacjenci), SUM(obrot_brutto), SUM(obrot_netto), SUM(zysk_netto)' \
                                f' FROM obroty_dzienne WHERE' \
                                f' data BETWEEN "{data_od}" AND "{data_do}"' \
                                f' AND apteka = {n}'
        obroty_archiwa_dane = zpt_queries.zpt_query_fetchall(guerry_obroty_archiwa)
        print(obroty_archiwa_dane)
        if not obroty_archiwa_dane or obroty_archiwa_dane == ((None, None, None, None),):
            obroty_archiwa_dict[f'{n}'] = [0, 0, 0, 0, 0, slowniki.online_id_nazwa[f'{n}']]

        else:
            marza = round((obroty_archiwa_dane[0][3] / obroty_archiwa_dane[0][2]) * 100, 2)
            obroty_archiwa_dict[f'{n}'] = [obroty_archiwa_dane[0][0],
                                           obroty_archiwa_dane[0][1],
                                           obroty_archiwa_dane[0][2],
                                           obroty_archiwa_dane[0][3],
                                           marza,
                                           slowniki.online_id_nazwa[f'{n}']]

            all_pacjenci += obroty_archiwa_dane[0][0]
            all_brutto += obroty_archiwa_dane[0][1]
            all_netto += obroty_archiwa_dane[0][2]
            all_zysk += obroty_archiwa_dane[0][3]
        if all_netto != 0:
            marza_all = round((all_zysk / all_netto) * 100, 2)
        else:
            marza_all = 0

    obroty_archiwa_dict[f'razem'] = [all_pacjenci, round(all_brutto, 2),
                                     round(all_netto, 2), round(all_zysk, 2), marza_all, 'RAZEM']

    return obroty_archiwa_dict

def tabela_archiwa(data_od, data_do):
    dane = get_dane_archiwa(data_od, data_do)
    tabela_header = f'<table width=100% style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" >' \
                    f'<tr>' \
                    f'<td width=16%  class="td_obroty" ><b>APTEKA</b></td>' \
                    f'<td width=16%  class="td_obroty"><b>PACJENCI</b></td>' \
                    f'<td width=16% class="td_obroty"><b>OBRÓT BRUTTO</b></td>' \
                    f'<td width=16% class="td_obroty"><b>OBRÓT NETTO</b></td>' \
                    f'<td width=16% class="td_obroty"><b>ZYSK NETTO</b></td>' \
                    f'<td width=20% class="td_obroty"><b>MARŻA</b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for n in range(2, 9):
        if n == 3:
            continue
        else:
            tabela_dane += f'<tr style="font-size: 12px;">' \
                           f'<td width=16%  class="td_obroty" >{dane[str(n)][5]}</td>' \
                           f'<td width=16%  class="td_obroty" >{dane[str(n)][0]}</td>' \
                           f'<td width=16%  class="td_obroty" >{fp.currency_format(dane[str(n)][1])} zł</td>' \
                           f'<td width=16%  class="td_obroty" >{fp.currency_format(dane[str(n)][2])} zł</td>' \
                           f'<td width=16%  class="td_obroty" >{fp.currency_format(dane[str(n)][3])} zł</td>' \
                           f'<td width=20%  class="td_obroty" >' \
                           f'{fp.currency_format(dane[str(n)][4])} %</td>' \
                           '</tr>'

    dane_razem = dane['razem']
    tabela_razem = f'<tr style = "background-color: #c34f4f; font-size:14px;">' \
                   f'<td width=16%  class="td_obroty" ><b>{dane_razem[5]}</b></td>' \
                   f'<td width=16%  class="td_obroty" ><b>{dane_razem[0]}</b></td>' \
                   f'<td width=16%  class="td_obroty" ><b>{fp.currency_format(dane_razem[1])} zł</b></td>' \
                   f'<td width=16%  class="td_obroty" ><b>{fp.currency_format(dane_razem[2])} zł</b></td>' \
                   f'<td width=16%  class="td_obroty" ><b>{fp.currency_format(dane_razem[3])} zł</b></td>' \
                   f'<td width=20%  class="td_obroty" ><b>' \
                   f'{fp.currency_format(dane_razem[4])} %</b></td>' \
                   '</tr>'

    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_razem + tabela_zakonczenie

    return tabela_koncowa
# SAGE
def tabela_wyciag(key):
    with open(staticfiles_storage.path('json/sage_wyciagi.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=10% ><b>LP</b></td>' \
                    f'<td width=12.5%><b>DATA</b></td>' \
                    f'<td width=30%><b>TYTUŁ</b></td>' \
                    f'<td width=12.5%><b>KWOTA</b></td>' \
                    f'<td width=12.5%><b>KONTO_WN</b></td>' \
                    f'<td width=12.5%><b>KONTO_MA</b></td>' \
                    f'<td width=10%><b></b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for d in dane[key]:
        data = dane[key][d]['data']
        tytul = dane[key][d]['tytul']
        kwota = dane[key][d]['kwota']
        konto_wn = dane[key][d]['konto_wn']
        konto_ma = dane[key][d]['konto_ma']
        style_color = ''
        if tytul == 'ZAPŁATA KARTĄ' or tytul == 'PROWIZJA/OPŁATA' or konto_wn == '404-3': #wpłata z terminali / prowizje
            style_color = 'style="color: #8c8787;"'
        elif tytul == 'PŁATNOŚĆ KARTĄ - ZAKUP' and konto_wn.endswith('-'): #zakup kartą bez kontrahenta
            style_color = 'style="color: #3068d1;"'
        elif tytul == 'PŁATNOŚĆ KARTĄ - ZAKUP' and konto_wn[-1] != '-': #zakup kartą z kontrahentem
            style_color = 'style="color: #eb5a00;"'
        elif tytul == 'WPŁATA GOTÓWKOWA': #wpłata gotówki w banku
            style_color = 'style="color: #3ea800;"'
        elif konto_wn == '' or konto_ma == '': #brak danych
            style_color = 'style="color: #c2041a;"'
        elif '(H)' in tytul: #przelew hurtownie
            style_color = 'style="color: #eba800;"'
        elif '(K)' in tytul: #przelew koszty
            style_color = 'style="color: #eb5a00;"'
        elif '(T)' in tytul: #przelew towar inny
            style_color = 'style="color: #fa7b2d;"'
        elif '200' in konto_ma or konto_ma == '149' or konto_ma == '145': #uznanie na rachunku
            style_color = 'style="color: #3ea800;"'
        elif konto_wn == '230' or konto_wn == '231': #wynagrodzenia
            style_color = 'style="color: #aaf2d3;"'
        elif 'PODATEK' in tytul or 'ZUS' in tytul or '221' in konto_wn: #podatki / ZUS
            style_color = 'style="color: #d95b63;"'
        elif 'PRZELEW ŚRODKÓW WŁASNYCH' in tytul: #przelew z innego banku
            style_color = 'style="color: #eb5a00;"'
        elif konto_wn == '134' or konto_ma == '134' or konto_wn == '137' or konto_ma == '137': #obciążenie rachunku inne
            style_color = 'style="color: #d95b63;"'

        tabela_dane += f'<tr  class="tr_edit" {style_color}>' \
                       f'<td width=10%>{d}</td>' \
                        f'<td width=12.5%>{data}</td>' \
                        f'<td width=30%>{tytul}</td>' \
                        f'<td width=12.5% >{kwota}</td>' \
                        f'<td width=12.5% >{konto_wn}</td>' \
                        f'<td width=12.5% >{konto_ma}</td>' \
                        f'<td width=10% >' \
                       f'<input type="hidden" name="wyciag_main_id" value="{key}">' \
                       f'<button class="button_edit_icon" type="submit" name="wyciag_pozycja_id" ' \
                       f'form="wyciag_edit" value="{d}">' \
                       f'<i class="bi bi-pencil-square"></i></button>' \
                       f'</td>' \
                       f'<tr>'
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_konta_specjalne():
    with open(staticfiles_storage.path('json/sage_konta_specjalne.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)
    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=10% ><b>LP</b></td>' \
                    f'<td width=30%><b>KONTO</b></td>' \
                    f'<td width=30%><b>TYTUŁ</b></td>' \
                    f'<td width=10%><b>KONTO WN</b></td>' \
                    f'<td width=10%><b>KONTO MA</b></td>' \
                    f'<td width=15%><b></b></td>' \
                    f'<tr>'

    tabela_dane = ''
    n = 1
    for key in dane:
        tabela_dane += f'<tr  class="tr_edit">' \
                       f'<td width=10%>{n}</td>' \
                       f'<td width=30%>{key}</td>' \
                       f'<td width=30%>{dane[key]["tytul"]}</td>' \
                       f'<td width=10% >{dane[key]["konto_wn"]}</td>' \
                       f'<td width=10% >{dane[key]["konto_ma"]}</td>' \
                       f'<td width=15% >' \
                       f'<button class="button_edit_icon" type="submit" name="konto_specjalne_delete_nr" ' \
                       f'form="konta_specjalne_edycja_delete" value="{key}">' \
                       f'<i class="bi bi-trash"></i></button>' \
                       f'</td>' \
                       f'<tr>'
        n += 1
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa

def tabela_kontrahenci_stali(rodzaj, fraza):
    with open(staticfiles_storage.path('json/sage_kontrahenci_stali.json'), "r", encoding='utf-8') as json_file:
        dane = json.load(json_file)

    tabela_header = f'<table style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" class="table">' \
                    f'<tr class="tr_header">' \
                    f'<td width=10% ><b>LP</b></td>' \
                    f'<td width=40%><b>NAZWA</b></td>' \
                    f'<td width=25%><b>NIP</b></td>' \
                    f'<td width=25%><b>ID SAGE</b></td>' \
                    f'<tr>'
    tabela_dane = ''
    n = 1
    if rodzaj == 'all':
        for key in dane:
            tabela_dane += f'<tr  class="tr_edit">' \
                           f'<td width=10%>{n}</td>' \
                           f'<td width=40%>{dane[key]["nazwa"]}</td>' \
                           f'<td width=25%>{key}</td>' \
                           f'<td width=25% >{dane[key]["id_kontrahenta"]}</td>' \
                           f'<tr>'
            n += 1

    if rodzaj == 'nazwa':
        for key in dane:
            if fraza.lower() in dane[key]['nazwa'].lower():
                tabela_dane += f'<tr  class="tr_edit">' \
                               f'<td width=10%>{n}</td>' \
                               f'<td width=40%>{dane[key]["nazwa"]}</td>' \
                               f'<td width=25%>{key}</td>' \
                               f'<td width=25% >{dane[key]["id_kontrahenta"]}</td>' \
                               f'<tr>'
                n += 1

    if rodzaj == 'nip':
        for key in dane:
            if fraza in key:
                tabela_dane += f'<tr  class="tr_edit">' \
                               f'<td width=10%>{n}</td>' \
                               f'<td width=40%>{dane[key]["nazwa"]}</td>' \
                               f'<td width=25%>{key}</td>' \
                               f'<td width=25% >{dane[key]["id_kontrahenta"]}</td>' \
                               f'<tr>'
                n += 1
    tabela_zakonczenie = '</table>'
    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa
# TABELE TESTY
def tabela_testowa_checkbox():
    dane = get_dane_przelewy_wykaz()
    tabela_header = f'<table width=80% style = "margin-left: auto; margin-right: auto; text-align: center;' \
                    f'    border-spacing: 0; border-collapse: collapse;" >' \
                    f'<tr>' \
                    f'<td width=5%  class="td_obroty"><b>ID</b></td>' \
                    f'<td width=25%  class="td_obroty"><b>KONTRAHENT</b></td>' \
                    f'<td width=15%  class="td_obroty"><b>DATA</b></td>' \
                    f'<td width=15% class="td_obroty"><b>KWOTA</b></td>' \
                    f'<td width=40% class="td_obroty"><b>TYTUŁ</b></td>' \
                    f'<tr>'

    tabela_dane = ''
    for d in dane:
        tabela_dane += f'<tr class="tr_edit" >' \
                       f'<td width=5%  class="td_obroty"><b>' \
                            f'<input class="form-check-input" type="checkbox" name="chceckbox_" value="{d[0]}">' \
                       f'</b></td>' \
                       f'<td width=25%  class="td_obroty"><b>{d[1]}</b></td>' \
                       f'<td width=15%  class="td_obroty"><b>{d[2]}</b></td>' \
                       f'<td width=15% class="td_obroty"><b>{d[3]} zł</b></td>' \
                       f'<td width=40% class="td_obroty"><b>{d[4]}</b></td>' \
                       f'<tr>'
    tabela_zakonczenie = '</table></br>'

    tabela_koncowa = tabela_header + tabela_dane + tabela_zakonczenie
    return tabela_koncowa