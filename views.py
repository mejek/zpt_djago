from django.shortcuts import render, redirect
import os
import datetime
from . import generator_tabeli
from . import funkcje_pomocnicze as fp
from . import biala_lista
from . import slowniki
from .forms import Gotowka_Form, Gotowka_Form_dodaj, Gotowka_Form_edytuj
from .forms import Koszty_Form_Faktury_dodaj, Koszty_Form_Faktury_edytuj
from .forms import Koszty_Form_Kontrahenci_dodaj, Koszty_Form_Kontrahenci_edytuj
from .forms import Towar_Dostawcy_Form_dodaj, Towar_Dostawcy_Form_edycja
from .forms import Hurtownie_Import_Danych, Hurtownie_Faktury, Hurtownie_Zestawienia
from .forms import Faktury_Form_wyszukaj, Przelewy_Szukaj_Form
from .forms import Form_Faktury_Wykaz_Kontrahent, Form_Faktury_Wykaz_Dostawca
from .forms import Pracownicy_Dane_Form, Pracownicy_Dane_Edycja_Form, Pracownicy_Nieobecnosci_dodaj_Form
from .forms import Rozne_fundusze_l_dodaj, Rozne_fundusze_l_edycja
from .forms import Rozne_karty_hallera_form, Rozne_czynsze, Form_Testy, Rozne_biala_lista_wyszukaj, Rozne_dyzury
from .forms import Form_reklamowiki, Form_todo
from .forms import Form_sage_wyciag_millenium, Form_sage_wyciag_pko, Form_sage_import_wyciag
from .forms import Form_sage_wyciag_edycja_pozycji, Form_sage_konta_specjalne_dodaj, Form_sage_kontrahenci_stali
from .forms import Form_archiwum_daty, Form_sage_rf_pliki

def home(request):
    return render(request, 'zpt_manager/home.html',
                  {
                        'title': 'HOME',
                        'alert_message': fp.alert_message(),
                        'footer_data': fp.footer_data(),
                        'active_link': fp.active_link_navbar(''),
                  }
                  )

def online(request):
    tabela_obroty_dzienne = generator_tabeli.tabela_obroty(generator_tabeli.get_dane_obroty_dzienne(), obroty='dzienne')
    tabela_obroty_miesieczne = generator_tabeli.tabela_obroty(generator_tabeli.get_dane_obroty_miesieczne(),
                                                               obroty='miesieczne')
    tabela_prognoza = generator_tabeli.tabela_prognoza(generator_tabeli.get_dane_prognoza())

    data_today = fp.data_today_with_time()
    data_miesiac_with_time = fp.data_miesiac_with_time()
    data_miesiac_today = fp.data_miesiac_today()

    return render(request, 'zpt_manager/online.html',
                  {
                      'title': 'ONLINE',
                      "data_today": data_today,
                      "data_miesiac_today": data_miesiac_today,
                      "data_miesiac_with_time": data_miesiac_with_time,
                      "tabela_obroty_dzienne": tabela_obroty_dzienne,
                      "tabela_obroty_miesieczne": tabela_obroty_miesieczne,
                      "tabela_prognoza": tabela_prognoza,
                      'alert_message': fp.alert_message(),
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('online'),

                  }
                  )

def gotowki(request):
    alert_message = fp.alert_message()
    form_gotowka_apteka = Gotowka_Form()
    form_gotowka_dodaj = Gotowka_Form_dodaj()
    form_gotowka_edytuj = Gotowka_Form_edytuj()
    form_edycja_display = 0
    apteka = '1'
    id_edycja = ''
    saldo = fp.get_saldo()
    tabela_gotowki = generator_tabeli.tabela_gotowki(apteka)

    if request.method == 'POST':
        if request.POST.get('data_gotowki_dodaj'):
            data_gotowki_dodaj = request.POST.get('data_gotowki_dodaj')
            apteka_gotowki_dodaj = request.POST.get('apteka_gotowki_dodaj')
            kwota_gotowki_dodaj = request.POST.get('kwota_gotowki_dodaj')
            opis_gotowki_dodaj = request.POST.get('opis_gotowki_dodaj')

            dane_gotowki_dodaj = [data_gotowki_dodaj, apteka_gotowki_dodaj, kwota_gotowki_dodaj, opis_gotowki_dodaj]
            fp.add_gotowki_to_zptdb(dane_gotowki_dodaj)
            saldo = fp.get_saldo()
            tabela_gotowki = generator_tabeli.tabela_gotowki(apteka)
            alert_message = fp.alert_message(f'Dodano pozycję gotówki:'
                                             f' {slowniki.gotowki_tabela[int(apteka_gotowki_dodaj)]}, kwota:'
                                              f' {kwota_gotowki_dodaj} zł')

        elif request.POST.get('lista_gotowki'):
            apteka = request.POST.get('lista_gotowki')
            saldo = ''
            tabela_gotowki = generator_tabeli.tabela_gotowki(apteka)
            form_gotowka_apteka.fields['lista_gotowki'].initial = apteka
            alert_message = fp.alert_message()

        #dodca buttony edycja i delete
        # logika do buttona edycja
        elif request.POST.get('gotowki_edycja_id'):
            id_edycja = request.POST.get('gotowki_edycja_id')
            form_edycja_display = 1
            saldo = ''
            tabela_gotowki = ''
            form_gotowka_apteka = ''
            dane = fp.get_data_gotowki_edycja(id_edycja)
            form_gotowka_edytuj.fields['data_gotowki_edutuj'].initial = dane[0]
            form_gotowka_edytuj.fields['apteka_gotowki_edutuj'].initial = dane[1]
            form_gotowka_edytuj.fields['kwota_gotowki_edutuj'].initial = dane[2]
            form_gotowka_edytuj.fields['opis_gotowki_edutuj'].initial = dane[3]


        elif request.POST.get('gotowki_usun_id'):
            id_usun = request.POST.get('gotowki_usun_id')
            fp.gotowki_delete(id_usun)
            alert_message = fp.alert_message(info=f'USUBIĘTO POZYCJĘ {id_usun}')
            saldo = fp.get_saldo()
            tabela_gotowki = generator_tabeli.tabela_gotowki(apteka)

        elif request.POST.get('data_gotowki_edutuj'):
            id_edycja = request.POST.get('id_edycja')
            data_gotowki_edutuj = request.POST.get('data_gotowki_edutuj')
            apteka_gotowki_edutuj = request.POST.get('apteka_gotowki_edutuj')
            kwota_gotowki_edutuj = request.POST.get('kwota_gotowki_edutuj')
            opis_gotowki_edutuj = request.POST.get('opis_gotowki_edutuj')

            data_to_update = [id_edycja, data_gotowki_edutuj, apteka_gotowki_edutuj,
                              kwota_gotowki_edutuj, opis_gotowki_edutuj]

            fp.update_gotowki(data_to_update)
            alert_message = fp.alert_message(f'Poprawiono pozycję gotówki (id {id_edycja}):'
                                             f' {slowniki.gotowki_tabela[int(apteka_gotowki_edutuj)]}, kwota: '
                                              f' {kwota_gotowki_edutuj} zł')
            saldo = fp.get_saldo()
            tabela_gotowki = generator_tabeli.tabela_gotowki(apteka)


    return render(request, 'zpt_manager/gotowki.html',
                  {
                      'title': 'GOTÓWKI',
                      'form_edycja_display': form_edycja_display,
                      'id_edycja': id_edycja,
                      'form_gotowka_apteka': form_gotowka_apteka,
                      'form_gotowka_dodaj': form_gotowka_dodaj,
                      'form_gotowka_edytuj': form_gotowka_edytuj,
                      'saldo': saldo,
                      'tabela_gotowki': tabela_gotowki,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('gotowki'),
                  }
                  )

# def gotowki_edycja(request, id_gotowki):
#
#     gotowka_form_edytuj = Gotowka_Form_edytuj()
#     #get data for id_gotowki from zpt
#     dane = fp.get_data_gotowki_edycja(id_gotowki)
#     gotowka_form_edytuj.fields['data_gotowki_edutuj'].initial = dane[0]
#     gotowka_form_edytuj.fields['apteka_gotowki_edutuj'].initial = f'{dane[1]}'
#     gotowka_form_edytuj.fields['kwota_gotowki_edutuj'].initial = f'{dane[2]}'
#     gotowka_form_edytuj.fields['opis_gotowki_edutuj'].initial = f'{dane[3]}'
#
#     return render(request, 'zpt_manager/gotowki_edycja.html',
#                   {
#                       'id_gotowki': id_gotowki,
#                       'gotowka_form_edytuj': gotowka_form_edytuj,
#                       'alert_message': fp.alert_message(),
#                       'footer_data': fp.footer_data(),
#                       'active_link': fp.active_link_navbar('gotowki'),
#                   })

def koszty_faktury(request):
    edycja_usun_display = ''
    alert_message = fp.alert_message()
    koszty_form_faktury_dodaj = Koszty_Form_Faktury_dodaj()
    koszty_form_edytuj = ''
    lista_kontrahentow = fp.get_lista_kontrahentow_koszty()
    id_koszty = ''


    if request.method == 'POST':
        if request.POST.get('koszty_faktury_kontrahent') and request.POST.get('koszty_faktury_kontrahent') != '0':
            koszty_dodaj_kontrahent = request.POST.get('koszty_faktury_kontrahent')
            koszty_dodaj_faktura = request.POST.get('koszty_faktury_faktura')
            koszty_dodaj_kwota = request.POST.get('koszty_faktury_kwota')
            koszty_dodaj_data = request.POST.get('koszty_faktury_data')
            # print(request.POST.getlist('chceckbox_'))
            dane_nowa_faktura = [int(koszty_dodaj_kontrahent), koszty_dodaj_faktura,
                                 f'{float(koszty_dodaj_kwota.replace(",",".")):0.2f}', koszty_dodaj_data]
            fp.add_koszty_to_zptdb(dane_nowa_faktura)
            alert_message = fp.alert_message(f'Dodano pozycję koszty: {koszty_dodaj_kontrahent} '
                                              f'{koszty_dodaj_faktura}')

        elif request.POST.get('koszty_edycja_id'):
            koszty_form_edytuj = Koszty_Form_Faktury_edytuj()
            edycja_usun_display = 1
            id_koszty = request.POST.get('koszty_edycja_id')
            dane = fp.get_data_koszty_edycja(id_koszty)
            koszty_form_edytuj.fields['koszty_faktury_kontrahent_edytuj'].initial = f'{dane[0]}'
            koszty_form_edytuj.fields['koszty_faktury_faktura_edytuj'].initial = f'{dane[1]}'
            koszty_form_edytuj.fields['koszty_faktury_kwota_edytuj'].initial = f'{dane[2]}'
            koszty_form_edytuj.fields['koszty_faktury_data_edytuj'].initial = f'{dane[3]}'

        elif request.POST.get('koszty_faktury_kontrahent_edytuj'):
            id_koszty = request.POST.get('id_koszty')
            koszty_edytuj_kontrahent = request.POST.get('koszty_faktury_kontrahent_edytuj')
            koszty_edytuj_faktura = request.POST.get('koszty_faktury_faktura_edytuj')
            koszty_edytuj_kwota = request.POST.get('koszty_faktury_kwota_edytuj').replace(',', '.')
            koszty_edytuj_data = request.POST.get('koszty_faktury_data_edytuj')

            dene_koszty_to_update = [id_koszty, koszty_edytuj_kontrahent, koszty_edytuj_faktura,
                                  koszty_edytuj_kwota, koszty_edytuj_data]
            fp.koszty_update(dene_koszty_to_update)
            alert_message = fp.alert_message(f'Poprawiono pozycję koszty: id {id_koszty}')

        elif request.POST.get('id_koszty_usun'):
            id_koszty_usun = request.POST.get('id_koszty_usun')
            fp.koszt_delete(id_koszty_usun)
            alert_message = fp.alert_message(f'Usunięto pozycję koszty: {id_koszty_usun}')

        elif request.POST.getlist('checkbox_') == []:
            alert_message = fp.alert_message('NIE WYBRANO ŻADNEJ FAKTURY', alert='warning')

        elif request.POST.getlist('checkbox_') != []:
            lista_do_bufora = request.POST.getlist('checkbox_')
            fp.dodaj_koszty_fakruty_do_bufora(lista_do_bufora)
            alert_message = fp.alert_message(f'FAKTURY ZOSTAŁY DODANE DO BUFORA')

    koszty_suma = fp.currency_format(fp.get_koszty_suma())
    tabela_koszty_do_zaplaty = generator_tabeli.tabela_koszty_do_zaplaty()

    return render(request, 'zpt_manager/koszty_faktury.html',
                  {
                      'title': 'KOSZTY FAKTURY',
                      'koszty_suma': koszty_suma,
                      'id_koszty': id_koszty,
                      'koszty_form_edytuj': koszty_form_edytuj,
                      'edycja_usun_display': edycja_usun_display,
                      'tabela_koszty_do_zaplaty': tabela_koszty_do_zaplaty,
                      'lista_kontrahentow': lista_kontrahentow,
                      'koszty_form_faktury_dodaj': koszty_form_faktury_dodaj,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('faktury'),
                  })

def koszty_kontrahenci(request):
    koszty_form_kontrahenci = Koszty_Form_Kontrahenci_dodaj()
    koszty_form_kontr_edycja = Koszty_Form_Kontrahenci_edytuj()
    alert_message = fp.alert_message()
    kontrahent_edyzja_display = ''
    tabela_kontrahenci_faktury_wykaz = ''
    id_kontrahent = ''

    if request.method == 'POST':
        if request.POST.get('koszty_kontr_nazwa_dodaj'):
            nazwa = request.POST.get('koszty_kontr_nazwa_dodaj')
            nip = request.POST.get('koszty_kontr_nip_dodaj')
            konto = request.POST.get('koszty_kontr_konto_dodaj')
            dane = [nazwa, nip, konto]
            fp.koszty_kontrahent_dodaj(dane)
            alert_message = fp.alert_message(f'Dodano nowego kontrahenta: {nazwa}')

        elif request.POST.get('koszty_kontr_nazwa_edytuj'):
            id_kontrahent =  request.POST.get('id_kontrahent')
            nazwa = request.POST.get('koszty_kontr_nazwa_edytuj')
            nip = request.POST.get('koszty_kontr_nip_edytuj')
            konto = request.POST.get('koszty_kontr_konto_edytuj')
            dane = [id_kontrahent, nazwa, nip, konto]
            fp.koszty_kontrahent_update(dane)
            alert_message = fp.alert_message(f'Zmioniono dane kontrahenta: {nazwa}')

        elif request.POST.get('id_koszty_kontrahent_usun'):
            id_koszty_kontrahent_usun = request.POST.get('id_koszty_kontrahent_usun')
            fp.koszty_kontrahent_delete(id_koszty_kontrahent_usun)
            alert_message = fp.alert_message(f'Usunięto pozycję kontrahenta: {id_koszty_kontrahent_usun}')

        elif request.POST.get('kontrahent_edytuj_id'):
            kontrahent_edyzja_display = 1
            id_kontrahent = request.POST.get('kontrahent_edytuj_id')
            dane = fp.get_dane_koszty_kontrahent_edycja(id_kontrahent)

            koszty_form_kontr_edycja.fields['koszty_kontr_nazwa_edytuj'].initial = f'{dane[0]}'
            koszty_form_kontr_edycja.fields['koszty_kontr_nip_edytuj'].initial = f'{dane[1]}'
            koszty_form_kontr_edycja.fields['koszty_kontr_konto_edytuj'].initial = f'{dane[2]}'

            try:
                if dane[1] != '' and dane[2] != '':
                    biala_lista_wynik = biala_lista.sprawdz_biala_lista(dane[1], dane[2])
                    if 'result' in str(biala_lista_wynik):
                        if biala_lista_wynik['result']['accountAssigned'] == 'TAK':
                            alert_message = fp.alert_message('Biała lista - OK', fade=False)
                    else:
                        alert_message = fp.alert_message(info='Biała lista - BŁĄD', alert='error', fade=False)
                else:
                    alert_message = fp.alert_message(info='BRAK DANYCH DO SPRAWDZENIA W BAZIE GOV', alert='warning',
                                                     fade=False)
            except:
                pass

            tabela_kontrahenci_faktury_wykaz = generator_tabeli.tabele_koszty_kontrahenci_faktury(id_kontrahent)

    tabela_kontrahenci = generator_tabeli.table_koszty_kontrahenci()

    return render(request, 'zpt_manager/koszty_kontrahenci.html',
                  {
                      'title': 'KONTRAHENCI',
                      'id_kontrahent': id_kontrahent,
                      'tabela_kontrahenci_faktury_wykaz': tabela_kontrahenci_faktury_wykaz,
                      'kontrahent_edyzja_display': kontrahent_edyzja_display,
                      'koszty_form_kontr_edycja': koszty_form_kontr_edycja,
                      'koszty_form_kontrahenci': koszty_form_kontrahenci,
                      'tabela_kontrahenci': tabela_kontrahenci,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('faktury'),
                  })

def faktury_wyszukaj(request):
    alert_message = fp.alert_message()
    form_faktury_wyszukaj = Faktury_Form_wyszukaj()
    tabela_faktury_wyszukaj = ''

    if request.method == 'POST':
        numer_faktury = request.POST.get('numer_faktury')
        tabela_faktury_wyszukaj = generator_tabeli.tabela_faktury_wyszukaj(numer_faktury)



    return render(request, 'zpt_manager/faktury_wyszukaj.html',
                  {
                      'title': 'FAKTURY SZUKAJ',
                      'tabela_faktury_wyszukaj': tabela_faktury_wyszukaj,
                      'form_faktury_wyszukaj':form_faktury_wyszukaj,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('faktury'),
                  })

def towar_faktury(request):

    if request.method == 'POST':
        if request.POST.getlist('checkbox_') == []:
            if not request.POST.get('towar_faktury_id'):
                alert_message = fp.alert_message('NIE WYBRANO ŻADNEJ FAKTURY', alert='warning')
            else:
                towar_faktura_id = request.POST.get('towar_faktury_id')
                alert_message = fp.alert_message(f'Oznaczono fakturę {towar_faktura_id} jako gotówkową.',
                                                 alert='information')
                fp.oznacz_towar_faktury_gotowka(towar_faktura_id)

        else:
            lista_do_bufora = request.POST.getlist('checkbox_')
            fp.dodaj_towar_fakruty_do_bufora(lista_do_bufora)
            alert_message = fp.alert_message(f'FAKTURY ZOSTAŁY DODANE DO BUFORA')
    else:
        alert_message = fp.alert_message()

    saldo = fp.currency_format(fp.get_faktury_towar_saldo())
    tabela_towar_faktury = generator_tabeli.tabele_towar_faktury()
    #todo kolory opóźnień w płatności

    return render(request, 'zpt_manager/towar_faktury.html',
                  {
                      'saldo': saldo,
                      'title': 'FAKTURY TOWAR',
                      'tabela_towar_faktury': tabela_towar_faktury,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('faktury'),
                  })

def towar_dostawcy(request):
    alert_message = fp.alert_message()
    towar_dostawcy_form = Towar_Dostawcy_Form_dodaj()
    form_towar_dostawcy_edycja = Towar_Dostawcy_Form_edycja()
    dostawca_edycja_display = ''
    id_dostawcy = ''
    tabela_towar_dostawcy_faktury = ''

    if request.method == 'POST':
        if request.POST.get('towar_dostawcy_nazwa_dodaj'):
            nazwa = request.POST.get('towar_dostawcy_nazwa_dodaj')
            nip = request.POST.get('towar_dostawcy_nip_dodaj')
            konto = request.POST.get('towar_dostawcy_konto_dodaj')
            if request.POST.get('towar_dostawcy_id_02_dodaj') != '':
                id_02 = int(request.POST.get('towar_dostawcy_id_02_dodaj'))
            else: id_02 = 0
            if request.POST.get('towar_dostawcy_id_04_dodaj') != '':
                id_04 = int(request.POST.get('towar_dostawcy_id_04_dodaj'))
            else: id_04 = 0
            if request.POST.get('towar_dostawcy_id_05_dodaj') != '':
                id_05 = int(request.POST.get('towar_dostawcy_id_05_dodaj'))
            else: id_05 = 0
            if request.POST.get('towar_dostawcy_id_06_dodaj') != '':
                id_06 = int(request.POST.get('towar_dostawcy_id_06_dodaj'))
            else: id_06 = 0
            if request.POST.get('towar_dostawcy_id_07_dodaj') != '':
                id_07 = int(request.POST.get('towar_dostawcy_id_07_dodaj'))
            else: id_07 = 0
            if request.POST.get('towar_dostawcy_id_08_dodaj') != '':
                id_08 = int(request.POST.get('towar_dostawcy_id_08_dodaj'))
            else: id_08 = 0
            dane = [nazwa, nip, konto, id_02, id_04, id_05, id_06, id_07, id_08]
            fp.towar_dostawcy_dodaj(dane)
            alert_message = fp.alert_message(f'Dodano nowego dostawcę: {nazwa}')

        elif request.POST.get('towar_dostawcy_nazwa_edycja'):
            id_dostawcy = request.POST.get('id_dostawcy')
            nazwa = request.POST.get('towar_dostawcy_nazwa_edycja')
            nip = request.POST.get('towar_dostawcy_nip_edycja')
            konto = request.POST.get('towar_dostawcy_konto_edycja')
            id_02 = request.POST.get('towar_dostawcy_id_02_edycja')
            id_04 = request.POST.get('towar_dostawcy_id_04_edycja')
            id_05 = request.POST.get('towar_dostawcy_id_05_edycja')
            id_06 = request.POST.get('towar_dostawcy_id_06_edycja')
            id_07 = request.POST.get('towar_dostawcy_id_07_edycja')
            id_08 = request.POST.get('towar_dostawcy_id_08_edycja')
            dane = [id_dostawcy, nazwa, nip, konto, id_02, id_04, id_05, id_06, id_07, id_08]
            fp.towar_dostawcy_edytuj(dane)
            alert_message = fp.alert_message(f'Poprawiono pozycję: {nazwa} ({id_dostawcy})')

        elif request.POST.get('id_towar_dostawcy_usun'):
            id_dostawcy_usun = request.POST.get('id_towar_dostawcy_usun')
            fp.towar_dostawcy_delete(id_dostawcy_usun)
            alert_message = fp.alert_message(f'Usunięto pozycję kontrahenta: {id_dostawcy_usun}')

        elif request.POST.get('dostawca_edytuj_id'):
            dostawca_edycja_display = 1
            id_dostawcy = request.POST.get('dostawca_edytuj_id')
            dane = fp.get_dane_towar_dostawcy_edycja(id_dostawcy)

            form_towar_dostawcy_edycja.fields['towar_dostawcy_nazwa_edycja'].initial = f'{dane[0]}'
            form_towar_dostawcy_edycja.fields['towar_dostawcy_nip_edycja'].initial = f'{dane[1]}'
            form_towar_dostawcy_edycja.fields['towar_dostawcy_konto_edycja'].initial = f'{dane[2]}'
            form_towar_dostawcy_edycja.fields['towar_dostawcy_id_02_edycja'].initial = f'{dane[3]}'
            form_towar_dostawcy_edycja.fields['towar_dostawcy_id_04_edycja'].initial = f'{dane[4]}'
            form_towar_dostawcy_edycja.fields['towar_dostawcy_id_05_edycja'].initial = f'{dane[5]}'
            form_towar_dostawcy_edycja.fields['towar_dostawcy_id_06_edycja'].initial = f'{dane[6]}'
            form_towar_dostawcy_edycja.fields['towar_dostawcy_id_07_edycja'].initial = f'{dane[7]}'
            form_towar_dostawcy_edycja.fields['towar_dostawcy_id_08_edycja'].initial = f'{dane[8]}'

            tabela_towar_dostawcy_faktury = generator_tabeli.tabela_towar_dostawcy_faktury(id_dostawcy)

    tabela_towar_dostawcy = generator_tabeli.tabela_towar_dostawcy()

    return render(request, 'zpt_manager/towar_dostawcy.html',
                  {
                      'title': 'DOSTAWCY',
                      'tabela_towar_dostawcy_faktury': tabela_towar_dostawcy_faktury,
                      'id_dostawcy': id_dostawcy,
                      'form_towar_dostawcy_edycja': form_towar_dostawcy_edycja,
                      'dostawca_edycja_display': dostawca_edycja_display,
                      'towar_dostawcy_form': towar_dostawcy_form,
                      'tabela_towar_dostawcy': tabela_towar_dostawcy,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('faktury'),
                  })

def faktury_wykaz(request):
    alert_message = fp.alert_message()
    form_faktury_wykaz_dostawca = Form_Faktury_Wykaz_Dostawca()
    form_faktury_wykaz_kontrahent = Form_Faktury_Wykaz_Kontrahent()
    tabela_faktury_wykaz = ''

    if request.method == 'POST':
        if request.POST.get('dostawca'):
            id_dostawcy = request.POST.get('dostawca')
            print(f'ID DASTAWCY: {id_dostawcy}')
            form_faktury_wykaz_dostawca.fields['dostawca'].initial = id_dostawcy
            tabela_faktury_wykaz = generator_tabeli.tabela_towar_dostawcy_faktury(id_dostawcy)

        elif request.POST.get('kontrahent'):
            id_kontrahent = request.POST.get('kontrahent')
            print(f'ID KONTRAHENT: {id_kontrahent}')
            form_faktury_wykaz_kontrahent.fields['kontrahent'].initial = id_kontrahent
            tabela_faktury_wykaz = generator_tabeli.tabele_koszty_kontrahenci_faktury(id_kontrahent)


    return render(request, 'zpt_manager/faktury_wykaz.html',
                  {
                      'title': 'FAKTURY WYKAZ',
                      'tabela_faktury_wykaz': tabela_faktury_wykaz,
                      'form_faktury_wykaz_dostawca': form_faktury_wykaz_dostawca,
                      'form_faktury_wykaz_kontrahent': form_faktury_wykaz_kontrahent,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('faktury'),
                  })

def przelewy_wykaz(request):
    form_przelewy_szukaj = Przelewy_Szukaj_Form()
    alert_message = fp.alert_message()
    tabela_przelewy_wykaz = ''
    fraza = ''
    szukaj_w = ''

    if request.method == 'POST':
        tytul_przelewu = request.POST.get('tytul_przelwu')
        odbiorca_przelwu = request.POST.get('odbiorca_przelwu')

        if tytul_przelewu != '':
            szukaj_w = 'tytul'
            fraza = tytul_przelewu
        elif odbiorca_przelwu != '':
            szukaj_w = 'odbiorca'
            fraza = odbiorca_przelwu

        tabela_przelewy_wykaz = generator_tabeli.tabela_przelewy_szukaj(fraza, szukaj_w)
        if tabela_przelewy_wykaz == '':
            alert_message = fp.alert_message(info='Musisz podać dane do wyszukania', alert='warning')

    else:
        tabela_przelewy_wykaz = generator_tabeli.tabela_przelewy_wykaz()


    return render(request, 'zpt_manager/przelewy_wykaz.html',
                  {
                      'title': 'PRZELEWY WYKAZ',
                      'form_przelewy_szukaj': form_przelewy_szukaj,
                      'tabela_przelewy_wykaz': tabela_przelewy_wykaz,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('przelewy'),
                  })

def przelewy_bufor(request):
    if request.method == 'POST':
        delete_bufor_id = request.POST.get('delete_bufor_id')
        if delete_bufor_id != None:
            fp.usun_towar_faktura_z_bufora(delete_bufor_id, czynnosc='DEL')
            alert_message = fp.alert_message('Faktura została usunięta z bufora')
        else:
            fp.eksport_przelwow_do_pliku()
            alert_message = fp.alert_message('Przelewy zostały wyeksportowane do pliku')

    else:
        alert_message = fp.alert_message()

    tabela_przelewy_bufor = generator_tabeli.tabela_przelewy_bufor()

    return render(request, 'zpt_manager/przelewy_bufor.html',
                  {
                      'title': 'BUFOR',
                      'saldo': fp.currency_format(tabela_przelewy_bufor[1]),
                      'tabela_przelewy_bufor': tabela_przelewy_bufor[0],
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('przelewy'),
                  })

def hurtownie_import_danych(request):
    path_desktop = r'C:\Users\dell\Desktop'
    plik = ''
    hurtownia = ''

    if request.method == 'POST':
        if request.POST.get('hurtownia') == '0':
            alert_message = fp.alert_message(alert='error', info='Musisz wybrać hurtownię')
        else:
            plik = request.POST.get('plik')
            plik_path = os.path.join(path_desktop, plik)
            fp.hurtownie_import_faktur(slowniki.hurtownie_import_dict[f"{request.POST.get('hurtownia')}"],plik_path)
            alert_message = fp.alert_message( info=f'{plik_path}')
            return redirect('hurtownie_faktury')
    else:

        alert_message = fp.alert_message()
        wynik_import = ''

    form_hurtownia_import_danych = Hurtownie_Import_Danych()
    return render(request, 'zpt_manager/hurtownie_import_danych.html',
                  {
                      'title': 'HURTOWNIE IMPORT',
                      'form_hurtownia_import_danych': form_hurtownia_import_danych,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('hurtownie'),
                  })

def hurtownie_faktury(request):
    sub = ''
    tabela_hurtownie_faktury = ''
    saldo = ''

    if request.method == 'POST':

        if request.POST.get('hurtownia') == '0':
            form_hurtownie_faktury = Hurtownie_Faktury()
            alert_message = fp.alert_message()

        else:
            form_hurtownie_faktury = Hurtownie_Faktury()
            hurtownia = request.POST.get('hurtownia')
            data = request.POST.get('data')
            form_hurtownie_faktury.fields['hurtownia'].initial = [hurtownia]
            form_hurtownie_faktury.fields['data'].initial = data
            dane_do_eksportu = generator_tabeli.get_dane_hurtownie_faktury(slowniki.hurtownie_import_dict[hurtownia])
            dane = generator_tabeli.tabela_hurtownie_fv(dane_do_eksportu, data)
            # print(dane)
            tabela_hurtownie_faktury = dane[0]
            saldo = dane[1]


            if request.POST.get('eksport') == 'EKSPORTUJ DO PLIKU' and hurtownia and data and saldo != '0.00':

                sub = generator_tabeli.tabela_hurtownie_zestawienie_eksport_do_pliku(
                    slowniki.hurtownie_import_dict[hurtownia], dane_do_eksportu, data)
                dane_z_eksportu = fp.eksportuj_do_hurtownie_zestawienia(slowniki.hurtownie_import_dict[hurtownia],
                                                                       dane_do_eksportu, data)
                id_zestawienia = dane_z_eksportu[0]
                saldo = dane_z_eksportu[1]

                fp.dodaj_hurtownie_przelew_do_bufora(slowniki.hurtownie_import_dict[hurtownia], saldo, id_zestawienia)
                form_hurtownie_faktury.fields['data'].initial = datetime.date.today()
                data = str(datetime.date.today())
                dane_do_eksportu = generator_tabeli.get_dane_hurtownie_faktury(
                    slowniki.hurtownie_import_dict[hurtownia])
                dane = generator_tabeli.tabela_hurtownie_fv(dane_do_eksportu, data)
                tabela_hurtownie_faktury = dane[0]
                saldo = dane[1]

            alert_message = fp.alert_message(sub)

    else:
        form_hurtownie_faktury = Hurtownie_Faktury()
        alert_message = fp.alert_message()



    return render(request, 'zpt_manager/hurtownie_faktury.html',
                  {
                      'title': 'HURTOWNIE FV',
                      'sub': sub,
                      'tabela_hurtownie_faktury': tabela_hurtownie_faktury,
                      'saldo': saldo,
                      'form_hurtownie_faktury': form_hurtownie_faktury,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('hurtownie'),
                  })

def hurtownie_zestawienia(request):
    form_hurtownie_zestawienia = Hurtownie_Zestawienia()
    alert_message = fp.alert_message()
    hurtownia = ''
    data = ''
    saldo = ''
    tabela_hurtownie_zestawienia = generator_tabeli.tabela_hurtownie_zestawienia(hurtownia)
    zestawienia_szczegoly_id = 0
    tabela_hurtownie_zestawienia_szczegoly = ''

    if request.method == 'POST':
        if request.POST.get('hurtownia'):
            hurtownia_id = request.POST.get('hurtownia')
            form_hurtownie_zestawienia.fields['hurtownia'].initial = [hurtownia_id]
            hurtownia = slowniki.hurtownie_import_dict[hurtownia_id]
            tabela_hurtownie_zestawienia = generator_tabeli.tabela_hurtownie_zestawienia(hurtownia)
            zestawienia_szczegoly_id = request.POST.get('zestawienia_szczegoly_id')

        elif request.POST.get('hurtownie_zestawienia_szczegoly_id'):
            zestawienia_szczegoly_id = request.POST.get('hurtownie_zestawienia_szczegoly_id')
            dane_zwrotne = generator_tabeli.tabela_hurtownie_zestawienia_szczegoly(zestawienia_szczegoly_id)
            saldo = dane_zwrotne['saldo']
            hurtownia = dane_zwrotne['hurtownia']
            data = dane_zwrotne['data']
            tabela_hurtownie_zestawienia_szczegoly = dane_zwrotne['tabela']

        elif request.POST.get('hurtownie_zestawienia_rozlicz_id'):
            zestawienie_rozlicz_id = request.POST.get('hurtownie_zestawienia_rozlicz_id')
            fp.rozlicz_przelew(zestawienie_rozlicz_id)

    return render(request, 'zpt_manager/hurtownie_zestawienia.html',
                  {
                      'title': 'HURTOWNIE ZESTAWIENIA',
                      'saldo': saldo,
                      'data': data,
                      'zestawienia_szczegoly_id': zestawienia_szczegoly_id,
                      'tabela_hurtownie_zestawienia': tabela_hurtownie_zestawienia,
                      'tabela_hurtownie_zestawienia_szczegoly': tabela_hurtownie_zestawienia_szczegoly,
                      'hurtownia': hurtownia,
                      'form_hurtownie_zestawienia':form_hurtownie_zestawienia,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('hurtownie'),
                  })

def hurtownie_poziom_zakupow(request):
    alert_message = fp.alert_message()
    miesiac = fp.get_miesiac_hurtownie_poziom_zakupow()[0]
    tabela_hurtownie_poziom_zakupow = generator_tabeli.tabela_hurtownie_poziom_zakupow(miesiac)

    return render(request, 'zpt_manager/hurtownie_poziom_zakupow.html',
                  {
                      'title': 'HURTOWNIE ZAKUPY',
                      'tabela_hurtownie_poziom_zakupow': tabela_hurtownie_poziom_zakupow,
                      'miesiac': miesiac,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('hurtownie'),
                  })

def hurtownie_maile(request):
    alert_message = fp.alert_message()

    if request.method == 'POST':
        if request.POST.get('wyslij_zestawienia'):
            dane = fp.get_dane_hurtownie_maile_wyslij_zestawienia()

            for z in dane:
                fp.wyslij_zestawienie_do_hurtowni(z)

        if request.POST.get('wyslij_zapytanie_zestawienia'):
            fp.wyslij_prosbe_o_zestawienie()

    tabela_wyslij_zestawienie = generator_tabeli.tabela_hurtownie_wyslij_zestawinie()

    return render(request, 'zpt_manager/hurtownie_maile.html',
                  {
                      'title': 'HURTOWNIE MAILE',
                      'tabela_wyslij_zestawienie': tabela_wyslij_zestawienie,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('hurtownie'),
                  })

def pracownicy_dane(request):
    alert_message = fp.alert_message()
    form_pracownicy_dane_wybor = Pracownicy_Dane_Form()
    tabela_pracownicy_dane = ''
    id_pracownika = '0'
    id_pracownika_edycja = ''
    form_pracownicy_dane_edycja = ''
    zapisz_zmiany_pracownicy_dane_id = ''

    if request.method == 'POST':
        if request.POST.get('lista_pracownikow'):
            id_pracownika = request.POST.get('lista_pracownikow')
            form_pracownicy_dane_wybor.fields['lista_pracownikow'].initial = [id_pracownika]
            tabela_pracownicy_dane = generator_tabeli.tabela_pracownicy_dane(id_pracownika)

        elif request.POST.get('pracownicy_dane_edycja_id'):
            id_pracownika_edycja = request.POST.get('pracownicy_dane_edycja_id')
            form_pracownicy_dane_wybor.fields['lista_pracownikow'].initial = [id_pracownika_edycja]
            form_pracownicy_dane_edycja = Pracownicy_Dane_Edycja_Form()
            dane = generator_tabeli.get_dane_pracownicy_dane(id_pracownika_edycja)
            form_pracownicy_dane_edycja.fields['imie'].initial = dane['imie']
            form_pracownicy_dane_edycja.fields['nazwisko'].initial = dane['nazwisko']
            form_pracownicy_dane_edycja.fields['pensja'].initial = dane['pensja']
            form_pracownicy_dane_edycja.fields['badania'].initial = dane['badania']
            form_pracownicy_dane_edycja.fields['data_zakonczenia_umowy'].initial = dane['data_zakonczenia_umowy']
            form_pracownicy_dane_edycja.fields['konto_bankowe'].initial = dane['konto_bankowe']
            form_pracownicy_dane_edycja.fields['stanowisko'].initial = dane['stanowisko']
            form_pracownicy_dane_edycja.fields['placowka'].initial = dane['placowka']
            if dane['aktywny'] == 'TAK':
                form_pracownicy_dane_edycja.fields['aktywny'].initial = ['0']
            else:
                form_pracownicy_dane_edycja.fields['aktywny'].initial = ['1']
            form_pracownicy_dane_edycja.fields['pranie'].initial = dane['pranie']
            form_pracownicy_dane_edycja.fields['premia'].initial = dane['premia']
            form_pracownicy_dane_edycja.fields['uwagi_wynagrodzenia'].initial = dane['uwagi_wynagrodzenia']
            form_pracownicy_dane_edycja.fields['data_urodzenia'].initial = dane['data_urodzenia']

        elif request.POST.get('pracownicy_dane_edycja_zapis_id'):

            id_pracownika = request.POST.get('pracownicy_dane_edycja_zapis_id')
            dane_do_zapisu = {}
            dane_do_zapisu['imie'] = request.POST.get('imie')
            dane_do_zapisu['nazwisko'] = request.POST.get('nazwisko')
            dane_do_zapisu['pensja'] = request.POST.get('pensja')
            dane_do_zapisu['badania'] = request.POST.get('badania')
            dane_do_zapisu['data_zakonczenia_umowy'] = request.POST.get('data_zakonczenia_umowy')
            dane_do_zapisu['konto_bankowe'] = request.POST.get('konto_bankowe')
            dane_do_zapisu['stanowisko'] = request.POST.get('stanowisko')
            dane_do_zapisu['placowka'] = request.POST.get('placowka')
            dane_do_zapisu['aktywny'] = request.POST.get('aktywny')
            dane_do_zapisu['pranie'] = request.POST.get('pranie')
            dane_do_zapisu['premia'] = request.POST.get('premia')
            dane_do_zapisu['uwagi_wynagrodzenia'] = request.POST.get('uwagi_wynagrodzenia')
            dane_do_zapisu['data_urodzenia'] = request.POST.get('data_urodzenia')
            fp.zapisz_zmiany_pracownicy_dane(id_pracownika, dane_do_zapisu)
            alert_message = fp.alert_message(info=f'POPRAWIONO DANE: {dane_do_zapisu["imie"]}'
                                                  f' {dane_do_zapisu["nazwisko"]}', alert='information')

            form_pracownicy_dane_wybor.fields['lista_pracownikow'].initial = [id_pracownika]
            tabela_pracownicy_dane = generator_tabeli.tabela_pracownicy_dane(id_pracownika)


    return render(request, 'zpt_manager/pracownicy_dane.html',
                  {
                      'title': 'PRACOWNICY',
                      'zapisz_zmiany_pracownicy_dane_id': zapisz_zmiany_pracownicy_dane_id,
                      'form_pracownicy_dane_edycja': form_pracownicy_dane_edycja,
                      'id_pracownika_edycja': id_pracownika_edycja,
                      'id_pracownika': id_pracownika,
                      'tabela_pracownicy_dane': tabela_pracownicy_dane,
                      'form_pracownicy_dane_wybor': form_pracownicy_dane_wybor,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('pracownicy'),
                  })

def pracownicy_urlopy(request):
    alert_message = fp.alert_message()
    form_pracownicy_urlopy_wybor = Pracownicy_Dane_Form()
    form_pracownicy_nieobecnosci_dodaj = Pracownicy_Nieobecnosci_dodaj_Form()
    id_pracownika = '0'
    tabela_pracowniy_urlopy = ''
    tabela_pracownicy_nieobecnosci_L4 = ''
    tabela_pracownicy_nieobecnosci_opieka_choroba = ''
    tabela_pracownicy_nieobecnosci_opieka_zdrowe_dziecko = ''
    tabela_pracownicy_nieobecnosci_urlop_okolicznosciowy = ''
    tabela_pracownicy_nieobecnosci_wolne_za_swieto = ''


    if request.method == 'POST':
        if request.POST.get('lista_pracownikow'):
            id_pracownika = request.POST.get('lista_pracownikow')
            form_pracownicy_urlopy_wybor.fields['lista_pracownikow'].initial = [id_pracownika]


            if id_pracownika != '0':
                if fp.sprawdz_status_pracownika(id_pracownika) == True:  # do dokończenia
                    pass
                else:
                    pass


        elif request.POST.get('id_pracownika_dodaj_nieobecnosc'):
            id_pracownika = request.POST.get('id_pracownika_dodaj_nieobecnosc')
            form_pracownicy_urlopy_wybor.fields['lista_pracownikow'].initial = [id_pracownika]
            #dodaj do danych nieobecnosci
            rodzaj_nioebecnosci = request.POST.get('rodzaj_nieobecnosci')
            data_od = request.POST.get('data_nieobecnosci_od')
            data_do = request.POST.get('data_nieobecnosci_do')
            uwagi = request.POST.get('uwagi')

            fp.pracownicy_nieobecnosci_dodaj(id_pracownika, rodzaj_nioebecnosci, data_od, data_do, uwagi)
            alert_message = fp.alert_message(info='DODANO NIEOBECNOŚĆ DO BAZY', alert='information')

        elif request.POST.get('pracownicy_usun_urlop'):
            id_pracownika = request.POST.get('pracownicy_usun_urlop')
            form_pracownicy_urlopy_wybor.fields['lista_pracownikow'].initial = [id_pracownika]
            fp.usun_ostatni_wpis_pracownicy_nieobecnosci(id_pracownika, '1')
            alert_message = fp.alert_message(info='USUNIĘTO OSTATNIĄ POZYCJĘ Z TABELI URLOPY')

        elif request.POST.get('pracownicy_usun_l4'):
            id_pracownika = request.POST.get('pracownicy_usun_l4')
            form_pracownicy_urlopy_wybor.fields['lista_pracownikow'].initial = [id_pracownika]
            fp.usun_ostatni_wpis_pracownicy_nieobecnosci(id_pracownika, '2')
            alert_message = fp.alert_message(info='USUNIĘTO OSTATNIĄ POZYCJĘ Z TABELI L4')

        elif request.POST.get('pracownicy_usun_opieka_chory'):
            id_pracownika = request.POST.get('pracownicy_usun_opieka_chory')
            form_pracownicy_urlopy_wybor.fields['lista_pracownikow'].initial = [id_pracownika]
            fp.usun_ostatni_wpis_pracownicy_nieobecnosci(id_pracownika, '3')
            alert_message = fp.alert_message(info='USUNIĘTO OSTATNIĄ POZYCJĘ Z TABELI OPIEKA CHORY')

        elif request.POST.get('pracownicy_usun_opieka_zdrowy'):
            id_pracownika = request.POST.get('pracownicy_usun_opieka_zdrowy')
            form_pracownicy_urlopy_wybor.fields['lista_pracownikow'].initial = [id_pracownika]
            fp.usun_ostatni_wpis_pracownicy_nieobecnosci(id_pracownika, '4')
            alert_message = fp.alert_message(info='USUNIĘTO OSTATNIĄ POZYCJĘ Z TABELI OPIEKA ZDROWY')

        elif request.POST.get('pracownicy_usun_okolicznosciowy'):
            id_pracownika = request.POST.get('pracownicy_usun_okolicznosciowy')
            form_pracownicy_urlopy_wybor.fields['lista_pracownikow'].initial = [id_pracownika]
            fp.usun_ostatni_wpis_pracownicy_nieobecnosci(id_pracownika, '5')
            alert_message = fp.alert_message(info='USUNIĘTO OSTATNIĄ POZYCJĘ Z TABELI URLOP OKOLICZNOŚCIOWY')

        elif request.POST.get('pracownicy_usun_wolne'):
            id_pracownika = request.POST.get('pracownicy_usun_wolne')
            form_pracownicy_urlopy_wybor.fields['lista_pracownikow'].initial = [id_pracownika]
            fp.usun_ostatni_wpis_pracownicy_nieobecnosci(id_pracownika, '7')
            alert_message = fp.alert_message(info='USUNIĘTO OSTATNIĄ POZYCJĘ Z TABELI WOLNE ZA ŚWIĘTA')


        dane_nieobecnosci = generator_tabeli.get_dane_pracownicy_urlopy(id_pracownika)
        tabela_pracowniy_urlopy = generator_tabeli.tabela_pracowniy_urlopy(dane_nieobecnosci)
        tabela_pracownicy_nieobecnosci_L4 = generator_tabeli.tabela_pracownicy_nieobecnosci_L4(dane_nieobecnosci['L4'])
        tabela_pracownicy_nieobecnosci_opieka_choroba = generator_tabeli.tabela_pracownicy_nieobecnosci_opieka_choroba(
            dane_nieobecnosci['opieka_choroba'])
        tabela_pracownicy_nieobecnosci_opieka_zdrowe_dziecko = generator_tabeli.tabela_pracownicy_nieobecnosci_opieka_zdrowe_dziecko(
            dane_nieobecnosci['opieka_zdrowe'])
        tabela_pracownicy_nieobecnosci_urlop_okolicznosciowy = generator_tabeli.tabela_pracownicy_nieobecnosci_urlop_okolicznosciowy(
            dane_nieobecnosci['urlop_okolicznosciowy'])
        tabela_pracownicy_nieobecnosci_wolne_za_swieto = generator_tabeli.tabela_pracownicy_nieobecnosci_wolne_za_swieto(
            dane_nieobecnosci['za_dzien_wolny'])

    return render(request, 'zpt_manager/pracownicy_urlopy.html',
                  {
                      'title': 'URLOPY',
                      'id_pracownika': id_pracownika,
                      'tabela_pracownicy_nieobecnosci_L4': tabela_pracownicy_nieobecnosci_L4,
                      'tabela_pracownicy_nieobecnosci_opieka_choroba': tabela_pracownicy_nieobecnosci_opieka_choroba,
                      'tabela_pracownicy_nieobecnosci_opieka_zdrowe_dziecko': tabela_pracownicy_nieobecnosci_opieka_zdrowe_dziecko,
                      'tabela_pracownicy_nieobecnosci_urlop_okolicznosciowy': tabela_pracownicy_nieobecnosci_urlop_okolicznosciowy,
                      'tabela_pracownicy_nieobecnosci_wolne_za_swieto': tabela_pracownicy_nieobecnosci_wolne_za_swieto,
                      'tabela_pracowniy_urlopy': tabela_pracowniy_urlopy,
                      'form_pracownicy_dane_wybor': form_pracownicy_urlopy_wybor,
                      'form_pracownicy_nieobecnosci_dodaj': form_pracownicy_nieobecnosci_dodaj,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('pracownicy'),
                  })

def pracownicy_wyplaty_dane(request):
    alert_message = fp.alert_message()
    pracownicy_wyplaty_dane = fp.get_pracownicy_dane_wyplata()
    miesiac_wyplaty = str(datetime.datetime.now())[:7]
    eksport = False

    if request.method == 'POST':
        dane_do_wyplaty = []
        for pracownik in pracownicy_wyplaty_dane:
            id_pracownika = pracownik['id_pracownika']
            nazwa = request.POST.get(f'pelna_nazwa_{id_pracownika}')
            pensja = request.POST.get(f'pensja_{id_pracownika}')
            uwagi = request.POST.get(f'uwagi_{id_pracownika}')
            urlopy = request.POST.get(f'urlopy_{id_pracownika}')
            premia = request.POST.get(f'premia_{id_pracownika}')
            pranie = request.POST.get(f'pranie_{id_pracownika}')
            dane_do_wyplaty.append({
                'nazwa': nazwa,
                'pensja': pensja,
                'uwagi': uwagi,
                'urlopy': urlopy,
                'premia': premia,
                'pranie': pranie,
            })

        eksport = fp.eksportuj_wynagrodzenia_do_pdf(dane_do_wyplaty, miesiac_wyplaty)


    return render(request, 'zpt_manager/pracownicy_wyplaty_dane.html',
                  {
                      'title': 'WYPŁATY DANE',
                      'eksport': eksport,
                      'miesiac_wyplaty': miesiac_wyplaty,
                      'pracownicy_wyplaty_dane': pracownicy_wyplaty_dane,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('pracownicy'),
                  })

def pracownicy_wyplaty_przelewy(request):
    alert_message = fp.alert_message()
    miesiac_wyplaty = str(datetime.datetime.now())[:7]
    dzien_wyplaty = fp.get_ostatni_dzien_miesiaca_do_wyplaty()
    eksport = False
    pracownicy_wyplaty_przelew = fp.get_pracownicy_wyplata_ostatni_przelew()

    if request.method == 'POST':
        eksport = True
        dane_do_przelewow = []
        for pracownik in pracownicy_wyplaty_przelew:
            wyplata = request.POST.get(f'ostatnia_wyplata_{pracownik["id_pracownika"]}')

            dane_do_przelewow.append({
                'id_pracownika': pracownik['id_pracownika'],
                'wyplata': wyplata,
                'konto_bankowe': pracownik['konto_bankowe'],
                'pelna_nazwa': pracownik['pelna_nazwa']
            })
        # zapisać ostatnia wypłata w pliku pracownicy.json
        fp.update_pracownicy_wyplata_ostatni_przelew(dane_do_przelewow)
        # zapisać przelewy do pliku
        fp.generuj_dane_do_pracownicy_przelewy_bank(dane_do_przelewow)


    return render(request, 'zpt_manager/pracownicy_wyplaty_przelewy.html',
                  {
                      'title': 'WYPŁATY PRZELEW',
                      'dzien_wyplaty': dzien_wyplaty,
                      'miesiac_wyplaty': miesiac_wyplaty,
                      'eksport': eksport,
                      'pracownicy_wyplaty_przelew': pracownicy_wyplaty_przelew,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('pracownicy'),
                  })

def pracownicy_wyplaty_zakupy_maile(request):
    alert_message = fp.alert_message()
    if request.method == 'POST':
        if request.POST.get('wyslij_zapytanie_dane_do_wyplaty'):
            fp.wyslij_prosbe_o_dane_do_wyplaty()
            alert_message = fp.alert_message('WYSŁANO PROŚBĘ O DANE DO WYPŁATY')


        if request.POST.get('wyslij_zapytanie_zakupy'):
            fp.wyslij_prosbe_o_zakupy()
            alert_message = fp.alert_message('WYSŁANO PROŚBĘ O LISTĘ ZAKUPÓW')


    return render(request, 'zpt_manager/pracownicy_wyplaty_zakupy_maile.html',
                  {
                      'title': 'MAILE',
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('pracownicy'),
                  })

def rozne_fundusze_l(request):
    alert_message = fp.alert_message()
    form_fundusze_l_dodaj = Rozne_fundusze_l_dodaj()
    form_fundusze_l_edycja = Rozne_fundusze_l_edycja()
    tabela_fundusze_l = generator_tabeli.tabela_fundusze_l()
    form_edycja_display = 0
    saldo = fp.fundusze_l_get_saldo()
    id_edycja = ''

    if request.method == 'POST':
        if request.POST.get('kwota'):
            data = request.POST.get('data')
            kwota = request.POST.get('kwota')
            opis = request.POST.get('opis')
            fp.fundusze_l_dodaj(data, kwota, opis)
            saldo = fp.fundusze_l_get_saldo()
            tabela_fundusze_l = generator_tabeli.tabela_fundusze_l()
            alert_message = fp.alert_message(info='DODANO NOWĄ POZYCJĘ')

        elif request.POST.get('fundusze_l_edycja_id'):
            form_edycja_display = 1
            id_edycja = request.POST.get('fundusze_l_edycja_id')
            tabela_fundusze_l = ''
            dane = fp.get_dane_fundusze_l_edycja(id_edycja)
            saldo = ''
            # print(dane)
            form_fundusze_l_edycja.fields['data_edycja'].initial = dane[1]
            form_fundusze_l_edycja.fields['kwota_edycja'].initial = dane[3]
            form_fundusze_l_edycja.fields['opis_edycja'].initial = dane[2]


        elif request.POST.get('fundusze_l_usun_id'):
            id_usun = request.POST.get('fundusze_l_usun_id')
            fp.fundusze_l_delete(id_usun)
            saldo = fp.fundusze_l_get_saldo()
            tabela_fundusze_l = generator_tabeli.tabela_fundusze_l()
            alert_message = fp.alert_message(info=f'USUBIĘTO POZYCJĘ {id_usun}')

        elif request.POST.get('kwota_edycja'):
            data = request.POST.get('data_edycja')
            kwota =request.POST.get('kwota_edycja')
            opis =request.POST.get('opis_edycja')
            id_edycja = request.POST.get('id_edycja')
            fp.fundusze_l_update(data, kwota, opis, id_edycja)
            saldo = fp.fundusze_l_get_saldo()
            tabela_fundusze_l = generator_tabeli.tabela_fundusze_l()
            alert_message = fp.alert_message(info=f'POPRAWIONO POZYCJĘ {id_edycja}')


    return render(request, 'zpt_manager/rozne_fundusze_l.html',
                  {
                      'title': 'GOTÓWKA',
                      'id_edycja': id_edycja,
                      'saldo': saldo,
                      'form_edycja_display': form_edycja_display,
                      'tabela_fundusze_l': tabela_fundusze_l,
                      'form_fundusze_l_dodaj': form_fundusze_l_dodaj,
                      'form_fundusze_l_edycja': form_fundusze_l_edycja,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('rozne'),
                  })

def rozne_karty_hallera(request):
    alert_message = fp.alert_message()
    fp.karty_hallera_uzupelnij_daty()
    fp.karty_hallera_uzupelnij_dane_z_kamsoft()
    form_karty_hallera_dodaj = Rozne_karty_hallera_form()
    form_edycja_display = 0
    tabela_karty_hallera = generator_tabeli.tabela_karty_hallera()

    if request.method == 'POST':
        if request.POST.get('data'):
            data = request.POST.get('data')
            kwota = request.POST.get('kwota')
            if fp.karty_hallera_dodaj(data, kwota) == True:
                fp.karty_hallera_uzupelnij_dane_z_kamsoft()
                alert_message = fp.alert_message(info=f'DODANO POZYCJĘ {data}: {kwota}')
            else:
                alert_message = fp.alert_message(info=f'BRAK DATY {data} W BAZIE', alert='error')
            tabela_karty_hallera = generator_tabeli.tabela_karty_hallera()


    return render(request, 'zpt_manager/rozne_karty_hallera.html',
                  {
                      'title': 'KARTY HALLERA',
                      'form_edycja_display': form_edycja_display,
                      'form_karty_hallera_dodaj': form_karty_hallera_dodaj,
                      'tabela_karty_hallera': tabela_karty_hallera,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('rozne'),
                  })

def rozne_czynsze(request):
    alert_message = fp.alert_message()
    tabela_czynsze = generator_tabeli.tabela_czynsze()
    id_rachunek = ''
    nowy_rachunek_nr = ''
    form_rozne_czynsze = ''
    nowy_key_dict = ''

    if request.method == 'POST':
        if request.POST.get('czynsze_do_skopiowania_id') or request.POST.get('czynsze_do_edycji_id'):
            form_rozne_czynsze = Rozne_czynsze()

            if request.POST.get('czynsze_do_skopiowania_id'):
                id_rachunek = request.POST.get('czynsze_do_skopiowania_id')
                nowy_rachunek_nr = fp.get_nowy_rachunek_nr()
                nowy_key_dict = fp.get_nowy_rachunek_key()
                dane_rachunek = fp.get_dane_rachunek(id_rachunek)
                form_rozne_czynsze.fields['nr_rachunku'].initial = nowy_rachunek_nr
            else:
                id_rachunek = request.POST.get('czynsze_do_edycji_id')
                nowy_rachunek_nr = fp.get_nowy_rachunek_nr()
                dane_rachunek = fp.get_dane_rachunek(id_rachunek)
                form_rozne_czynsze.fields['nr_rachunku'].initial = dane_rachunek['nr']

            kontrahent_key = fp.get_kontrahent_key(id_rachunek)

            form_rozne_czynsze.fields['data'].initial = dane_rachunek['data']
            form_rozne_czynsze.fields['kontrahent'].initial = kontrahent_key
            form_rozne_czynsze.fields['pole_1'].initial = dane_rachunek['pole_1']
            form_rozne_czynsze.fields['pole_2'].initial = dane_rachunek['pole_2']
            form_rozne_czynsze.fields['pole_3'].initial = dane_rachunek['pole_3']
            form_rozne_czynsze.fields['pole_4'].initial = dane_rachunek['pole_4']
            form_rozne_czynsze.fields['pole_5'].initial = dane_rachunek['pole_5']
            form_rozne_czynsze.fields['kwota_1'].initial = dane_rachunek['kwota_1']
            form_rozne_czynsze.fields['kwota_2'].initial = dane_rachunek['kwota_2']
            form_rozne_czynsze.fields['kwota_3'].initial = dane_rachunek['kwota_3']
            form_rozne_czynsze.fields['kwota_4'].initial = dane_rachunek['kwota_4']
            form_rozne_czynsze.fields['kwota_5'].initial = dane_rachunek['kwota_5']
            suma = round(float(dane_rachunek['kwota_1']) + float(dane_rachunek['kwota_2']) + \
                   float(dane_rachunek['kwota_3']) + float(dane_rachunek['kwota_4']) + \
                         float(dane_rachunek['kwota_5']), 2)
            form_rozne_czynsze.fields['suma'].initial = suma

        #dodawanie nowego rachunku
        elif request.POST.get('nowy_rachunek_key') or request.POST.get('id_rachunek_edycja'):

            dane_dict = {}
            dane_dict['nr'] = request.POST.get('nr_rachunku')
            dane_dict['data'] = request.POST.get('data')
            dane_dict['najemca'] = slowniki.czynsze_kontrahenci_dict[request.POST.get('kontrahent')]['nazwa']
            dane_dict['pole_1'] = request.POST.get('pole_1')
            dane_dict['pole_2'] = request.POST.get('pole_2')
            dane_dict['pole_3'] = request.POST.get('pole_3')
            dane_dict['pole_4'] = request.POST.get('pole_4')
            dane_dict['pole_5'] = request.POST.get('pole_5')
            dane_dict['kwota_1'] = round(float(request.POST.get('kwota_1').replace(',','.')),2)
            dane_dict['kwota_2'] = round(float(request.POST.get('kwota_2').replace(',','.')),2)
            dane_dict['kwota_3'] = round(float(request.POST.get('kwota_3').replace(',','.')),2)
            dane_dict['kwota_4'] = round(float(request.POST.get('kwota_4').replace(',','.')),2)
            dane_dict['kwota_5'] = round(float(request.POST.get('kwota_5').replace(',','.')),2)
            dane_dict['suma'] = round(float(request.POST.get('suma')),2)
            dane_dict['licznik'] = 0


            if request.POST.get('nowy_rachunek_key'):
                nowy_rachunek_key = request.POST.get('nowy_rachunek_key')
                dane_dict['mail'] = 0
                fp.zapisz_zmiany_w_pliku_czynsze(nowy_rachunek_key, dane_dict)
                alert_message = fp.alert_message('DODANO NOWY RACHUNEK')

            elif request.POST.get('id_rachunek_edycja'):
                rachunek_key_edycja = request.POST.get('id_rachunek_edycja')
                dane_dict['mail'] = fp.oznaczenie_mail(rachunek_key_edycja)
                fp.zapisz_zmiany_w_pliku_czynsze(rachunek_key_edycja, dane_dict)
                alert_message = fp.alert_message('ZMIENIONO DANE NA RACHUNKU')

            tabela_czynsze = generator_tabeli.tabela_czynsze()

        elif request.POST.get('czynsze_do_wyslania_mailem_id'):
            id_rachunek = request.POST.get('czynsze_do_wyslania_mailem_id')
            mail = fp.czynsze_wyslij_mailem(id_rachunek)
            fp.zmien_oznaczenie_mail(id_rachunek)
            tabela_czynsze = generator_tabeli.tabela_czynsze()
            alert_message = fp.alert_message(f'WYSŁANO RACHUBEK {mail[0]} do {mail[1]}')
            id_rachunek = ''

        elif request.POST.get('pdf_id'):
            id_rachunek = request.POST.get('pdf_id')
            fp.eksportuj_rachunek_czynsz_pdf(id_rachunek)
            tabela_czynsze = generator_tabeli.tabela_czynsze()
            alert_message = fp.alert_message('ZAPISANO RACHUNEK DO PLIKU')
            id_rachunek = ''


    return render(request, 'zpt_manager/rozne_czynsze.html',
                  {
                      'title': 'CZYNSZE',
                      'nowy_key_dict': nowy_key_dict,
                      'form_rozne_czynsze': form_rozne_czynsze,
                      'nowy_rachunek_id': nowy_rachunek_nr,
                      'id_rachunek': id_rachunek,
                      'tabela_czynsze': tabela_czynsze,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('rozne'),
                  })

def rozne_biala_lista(request):
    alert_message = fp.alert_message()
    form_biala_lista_wyszukaj = Rozne_biala_lista_wyszukaj()
    nazwa_szukana = ''

    if request.method == 'POST':
        if request.POST.get('nazwa'):
            nazwa_szukana = request.POST.get('nazwa')

    tabela_biala_lista = generator_tabeli.tabela_biala_lista(nazwa_szukana)

    return render(request, 'zpt_manager/rozne_biala_lista.html',
                  {
                      'title': 'BIAŁA LISTA',
                      'tabela_biala_lista': tabela_biala_lista,
                      'form_biala_lista_wyszukaj': form_biala_lista_wyszukaj,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('rozne'),
                  })

def rozne_dyzury(request):
    alert_message = fp.alert_message()
    form_rozne_dyzury = Rozne_dyzury()
    wyslij_button_display = False
    tabela_dyzury = ''
    data_stop = ''
    data_start = ''

    if request.method == 'POST':
        if request.POST.get('data_start'):
            data_start = request.POST.get('data_start')
            data_stop = request.POST.get('data_stop')
            form_rozne_dyzury.fields['data_start'].initial = data_start
            form_rozne_dyzury.fields['data_stop'].initial = data_stop
            wyslij_button_display = True
            lista_dat_dyzury = fp.get_lista_dat_dyzury(data_start, data_stop)
            tabela_dyzury = generator_tabeli.tabela_dyzury(lista_dat_dyzury)
            fp.dyzury_generuj_pdf(lista_dat_dyzury)

    #wysyłanie zestawienia do aptek
        elif request.POST.get('wyslij_email'):
            data_start = request.POST.get('data_start_mail')
            data_stop = request.POST.get('data_stop_mail')
            if fp.dyzury_wyslij_emailem(data_start, data_stop) == True:
                alert_message = fp.alert_message('WYSŁANO ZESTAWIENIE DYŻURÓW DO APTEK')
            else:
                alert_message = fp.alert_message('PRÓBA WYSŁANIA ZESTAWIENIA DO APTEK NIE POWIODŁA SIĘ', alert='error')


    return render(request, 'zpt_manager/rozne_dyzury.html',
                  {
                      'title': 'DYŻURY',
                      'data_start': data_start,
                      'data_stop': data_stop,
                      'tabela_dyzury': tabela_dyzury,
                      'wyslij_button_display': wyslij_button_display,
                      'form_rozne_dyzury': form_rozne_dyzury,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('rozne'),
                  })

def rozne_reklamowki(request):
    alert_message = fp.alert_message()
    form_reklamowki = Form_reklamowiki()
    tabela_reklamowki_raport = ''

    if request.method == 'POST':
        kwartal_id = request.POST.get('kwartal')
        rok = request.POST.get('rok')
        tabela_reklamowki_raport = generator_tabeli.tabela_reklamowki_raport(kwartal_id, rok)
        form_reklamowki.fields['kwartal'].initial = kwartal_id
        form_reklamowki.fields['rok'].initial = rok



    return render(request, 'zpt_manager/rozne_reklamowki.html',
                  {
                      'title': 'REKLAMÓWKI',
                      'tabela_reklamowki_raport': tabela_reklamowki_raport,
                      'form_reklamowki': form_reklamowki,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('rozne'),
                  })

def rozne_todo_list(request):
    alert_message = fp.alert_message()
    done_undone_button = ''
    todo_task_id = ''
    form_todo = Form_todo()

    if not request.method == 'POST':
        tabela_todo_list = generator_tabeli.tabela_todo_list()
        tabela_todo_list_done = generator_tabeli.tabela_todo_list_done()
        display_mode = 'table'

    elif request.method == 'POST':
        tabela_todo_list = ''
        tabela_todo_list_done = ''
        display_mode = 'edit'

        if request.POST.get('todo_edit_id') or request.POST.get('done_edit_id'):
            if request.POST.get('todo_edit_id'):
                done_undone_button = 'finish'
                todo_task_id = request.POST.get('todo_edit_id')

            elif request.POST.get('done_edit_id'):
                done_undone_button = 'undo'
                todo_task_id = request.POST.get('done_edit_id')
            task_dane = fp.get_dane_todo_task(todo_task_id)
            form_todo.fields['opis'].initial = task_dane['opis']
            form_todo.fields['nazwa'].initial = task_dane['nazwa']
            form_todo.fields['data_dodania'].initial = task_dane['data_dodania']
            form_todo.fields['termin'].initial = task_dane['termin']


        elif request.POST.get('zapisz_zmiany'):
            todo_task_id = request.POST.get('zapisz_zmiany')

            opis = request.POST.get('opis')
            nazwa = request.POST.get('nazwa')
            data_dodania = request.POST.get('data_dodania')
            termin = request.POST.get('termin')
            fp.update_todo_task(todo_task_id, nazwa, opis, data_dodania, termin)
            alert_message = fp.alert_message('ZAPISANO ZMIANY W ZADANIU')
            tabela_todo_list = generator_tabeli.tabela_todo_list()
            tabela_todo_list_done = generator_tabeli.tabela_todo_list_done()
            display_mode = 'table'

        elif request.POST.get('zakoncz'):
            opis = request.POST.get('opis')
            nazwa = request.POST.get('nazwa')
            data_dodania = request.POST.get('data_dodania')
            termin = request.POST.get('termin')
            todo_task_id = request.POST.get('todo_task_id')
            fp.update_todo_task(todo_task_id, nazwa, opis, data_dodania, termin)
            fp.rozne_todo_zakoncz_zadanie(todo_task_id)
            alert_message = fp.alert_message('ZADANIE ZOSTAŁO ZAKOŃCZONE')
            tabela_todo_list = generator_tabeli.tabela_todo_list()
            tabela_todo_list_done = generator_tabeli.tabela_todo_list_done()
            display_mode = 'table'

        elif request.POST.get('undo'):
            todo_task_id = request.POST.get('todo_task_id')
            fp.rozne_todo_undone_zadanie(todo_task_id)
            alert_message = fp.alert_message('ZADANIE ZOSTAŁO PRZYWRÓCONE DO NIEZAKOŃCZONYCH')
            tabela_todo_list = generator_tabeli.tabela_todo_list()
            tabela_todo_list_done = generator_tabeli.tabela_todo_list_done()
            display_mode = 'table'

        elif request.POST.get('todo_nowy'):
            todo_task_id = fp.get_new_todo_task_id()

        elif request.POST.get('todo_delete_id'):
            todo_task_id = request.POST.get('todo_delete_id')
            fp.delete_todo_task(todo_task_id)
            alert_message = fp.alert_message('USUNIĘTO ZADANIE Z LISTY')
            tabela_todo_list = generator_tabeli.tabela_todo_list()
            tabela_todo_list_done = generator_tabeli.tabela_todo_list_done()
            display_mode = 'table'



    return render(request, 'zpt_manager/rozne_todo_list.html',
                  {
                      'title': 'TO DO',
                      'form_todo': form_todo,
                      'todo_task_id': todo_task_id,
                      'done_undone_button': done_undone_button,
                      'display_mode': display_mode,
                      'tabela_todo_list': tabela_todo_list,
                      'tabela_todo_list_done': tabela_todo_list_done,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('rozne'),
                  })

def rozne_archiwa(request):
    alert_message = fp.alert_message()
    form_archiwum_daty = Form_archiwum_daty()
    tabela_archiwa = ''

    if request.method == 'POST':
        if request.POST.get('data_od'):
            data_od = request.POST.get('data_od')
            data_do = request.POST.get('data_do')

            tabela_archiwa = generator_tabeli.tabela_archiwa(data_od, data_do)
            form_archiwum_daty.fields['data_od'].initial = data_od
            form_archiwum_daty.fields['data_do'].initial = data_do


    return render(request, 'zpt_manager/rozne_archiwa.html',
                  {
                      'title': 'ARCHIWA',
                      'tabela_archiwa': tabela_archiwa,
                      'form_archiwum_daty': form_archiwum_daty,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('rozne'),
                  })
# SAGE
def sage_wyciagi(request):
    alert_message = fp.alert_message()
    form_wyciag_millenium_id = Form_sage_wyciag_millenium()
    form_wyciag_pko_id = Form_sage_wyciag_pko()
    lista_wyboru_millenium = fp.get_lista_wyciagow('MIL')
    lista_wyboru_pko = fp.get_lista_wyciagow('PKO')
    form_sage_wyciag_edycja_pozycji = ''
    wyciag_key = ''
    wyciag_pozycja_id = ''
    wyciag_main_id = ''
    dane_pozycja_wyciag = ''
    edit_display = 0

    form_wyciag_millenium_id.fields['wyciag_millenium_id'].choices = lista_wyboru_millenium
    form_wyciag_pko_id.fields['wyciag_pko_id'].choices = lista_wyboru_pko

    if request.method == 'POST':
        if request.POST.get('wyciag_millenium_id'):
            print('MIL')
            wyciag_id = request.POST.get('wyciag_millenium_id')
            wyciag_key = fp.get_wyciag_key(wyciag_id, lista_wyboru_millenium)
            form_wyciag_millenium_id.fields['wyciag_millenium_id'].initial = wyciag_id

        elif request.POST.get('wyciag_pko_id'):
            print('PKO')
            wyciag_id = request.POST.get('wyciag_pko_id')
            wyciag_key = fp.get_wyciag_key(wyciag_id, lista_wyboru_pko)
            form_wyciag_pko_id.fields['wyciag_pko_id'].initial = wyciag_id

        elif request.POST.get('wyciag_pozycja_id'):
            wyciag_pozycja_id = request.POST.get('wyciag_pozycja_id')
            wyciag_main_id = request.POST.get('wyciag_main_id')
            edit_display = 1
            dane_pozycja_wyciag = fp.get_dane_pozycja_wyciag(wyciag_main_id, wyciag_pozycja_id)
            form_sage_wyciag_edycja_pozycji = Form_sage_wyciag_edycja_pozycji()
            form_sage_wyciag_edycja_pozycji.fields['wyciag'].initial = wyciag_main_id
            form_sage_wyciag_edycja_pozycji.fields['nr_transakcji'].initial = wyciag_pozycja_id
            form_sage_wyciag_edycja_pozycji.fields['data'].initial = dane_pozycja_wyciag['data']
            form_sage_wyciag_edycja_pozycji.fields['tytul'].initial = dane_pozycja_wyciag['tytul']
            form_sage_wyciag_edycja_pozycji.fields['kontrahent'].initial = dane_pozycja_wyciag['kontrahent']
            form_sage_wyciag_edycja_pozycji.fields['kwota'].initial = dane_pozycja_wyciag['kwota']
            form_sage_wyciag_edycja_pozycji.fields['nip'].initial = dane_pozycja_wyciag['nip']
            form_sage_wyciag_edycja_pozycji.fields['konto_wn'].initial = dane_pozycja_wyciag['konto_wn']
            form_sage_wyciag_edycja_pozycji.fields['konto_ma'].initial = dane_pozycja_wyciag['konto_ma']
            form_sage_wyciag_edycja_pozycji.fields['id_sage'].initial = dane_pozycja_wyciag['id_sage']
            form_sage_wyciag_edycja_pozycji.fields['rachunek'].initial = dane_pozycja_wyciag['rachunek']
            form_sage_wyciag_edycja_pozycji.fields['konto_spec'].initial = dane_pozycja_wyciag['konto_spec']
            form_sage_wyciag_edycja_pozycji.fields['rodzaj'].initial = dane_pozycja_wyciag['rodzaj']

        elif request.POST.get('sage_wyciag_edycja_pozycji_zapisz_id'):
            wyciag_main_id = request.POST.get('wyciag')
            wyciag_pozycja_id = request.POST.get('nr_transakcji')

            dane_pozycji_do_zapisu = {}
            dane_pozycji_do_zapisu["data"] = request.POST.get('data')
            dane_pozycji_do_zapisu["tytul"] = request.POST.get('tytul')
            dane_pozycji_do_zapisu["kontrahent"] = request.POST.get('kontrahent')
            dane_pozycji_do_zapisu["kwota"] = request.POST.get('kwota')
            dane_pozycji_do_zapisu["nip"] = request.POST.get('nip')
            dane_pozycji_do_zapisu["konto_wn"] = request.POST.get('konto_wn')
            dane_pozycji_do_zapisu["konto_ma"] = request.POST.get('konto_ma')
            dane_pozycji_do_zapisu["id_sage"] = request.POST.get('id_sage')
            dane_pozycji_do_zapisu["rachunek"] = request.POST.get('rachunek')
            dane_pozycji_do_zapisu["konto_spec"] = request.POST.get('konto_spec')
            dane_pozycji_do_zapisu["rodzaj"] = request.POST.get('rodzaj')

            # print(dane_pozycji_do_zapisu)
            fp.zapisz_dane_pozycja_wyciag(wyciag_main_id, wyciag_pozycja_id, dane_pozycji_do_zapisu)

            alert_message = fp.alert_message(f'POPRWIONO POZYCJĘ {wyciag_main_id} / {wyciag_pozycja_id}')

            if 'MIL' in wyciag_main_id:
                wyciag_key = wyciag_main_id
                form_wyciag_millenium_id.fields['wyciag_millenium_id'].initial = fp.get_lista_wyboru_id(wyciag_key, lista_wyboru_millenium)
            elif 'PKO' in wyciag_main_id:
                wyciag_key = wyciag_main_id
                form_wyciag_pko_id.fields['wyciag_pko_id'].initial = fp.get_lista_wyboru_id(wyciag_key, lista_wyboru_pko)

    if wyciag_key != '':
        tabela_wyciag = generator_tabeli.tabela_wyciag(wyciag_key)
    else:
        tabela_wyciag = ''

    return render(request, 'zpt_manager/sage_wyciagi.html',
                  {
                      'title': 'SAGE WYCIĄGI',
                      'form_sage_wyciag_edycja_pozycji': form_sage_wyciag_edycja_pozycji,
                      'dane_pozycja_wyciag': dane_pozycja_wyciag,
                      'edit_display': edit_display,
                      'wyciag_main_id': wyciag_main_id,
                      'wyciag_pozycja_id': wyciag_pozycja_id,
                      'tabela_wyciag': tabela_wyciag,
                      'form_wyciag_millenium_id': form_wyciag_millenium_id,
                      'form_wyciag_pko_id': form_wyciag_pko_id,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('sage'),
                  })

def sage_nowy_wyciag(request):
    alert_message = fp.alert_message()
    form_sage_import_wyciag = Form_sage_import_wyciag()
    wyciagi_path = r'C:\Users\dell\Dysk Google\IMPORTY\WYCIĄGI'
    bank = ''
    dane_do_wyciagu = ''
    plik = ''
    plik_path = ''

    if request.method == 'POST':
        if request.POST.get('plik'):
            plik = request.POST.get('plik')
            plik_path = os.path.join(wyciagi_path, plik)

            bank = plik[:3]
            if bank == 'MIL':
                dane_do_wyciagu = fp.mt940_parser(plik_path)
            if bank == 'PKO':
                dane_do_wyciagu = fp.pko_parser(plik_path)

            fp.dodaj_wyciag(dane_do_wyciagu, plik[:-4])
            return redirect('wyciagi')


    return render(request, 'zpt_manager/sage_nowy_wyciag.html',
                  {
                      'title': 'SAGE NOWY WYCIĄG',
                      'dane_do_wyciagu': dane_do_wyciagu,
                      'bank': bank,
                      'plik': plik_path,
                      'form_sage_import_wyciag': form_sage_import_wyciag,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('sage'),
                  })

def sage_eksport(request):
    alert_message = fp.alert_message()
    form_wyciag_millenium_id = Form_sage_wyciag_millenium()
    form_wyciag_pko_id = Form_sage_wyciag_pko()
    lista_wyboru_millenium = fp.get_lista_wyciagow('MIL')
    lista_wyboru_pko = fp.get_lista_wyciagow('PKO')
    form_wyciag_millenium_id.fields['wyciag_millenium_id'].choices = lista_wyboru_millenium
    form_wyciag_pko_id.fields['wyciag_pko_id'].choices = lista_wyboru_pko
    wyciag_key = ''

    if request.method == 'POST':
        if request.POST.get('wyciag_millenium_id'):
            wyciag_id = request.POST.get('wyciag_millenium_id')
            wyciag_key = fp.get_wyciag_key(wyciag_id, lista_wyboru_millenium)
            form_wyciag_millenium_id.fields['wyciag_millenium_id'].initial = wyciag_id

        elif request.POST.get('wyciag_pko_id'):
            wyciag_id = request.POST.get('wyciag_pko_id')
            wyciag_key = fp.get_wyciag_key(wyciag_id, lista_wyboru_pko)
            form_wyciag_pko_id.fields['wyciag_pko_id'].initial = wyciag_id

        elif request.POST.get('eksportuj_wyciag'):
            wyciag_key_eksport = request.POST.get('eksportuj_wyciag')
            fp.eksportuj_wyciag_do_sage(wyciag_key_eksport)

    return render(request, 'zpt_manager/sage_eksport.html',
                  {
                      'title': 'SAGE EKSPORT',
                      'wyciag_key': wyciag_key,
                      'form_wyciag_millenium_id': form_wyciag_millenium_id,
                      'form_wyciag_pko_id': form_wyciag_pko_id,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('sage'),
                  })

def sage_konta_specjalne(request):
    alert_message = fp.alert_message()
    form_edycja_display = 0
    form_konto_specjalne_dodaj = Form_sage_konta_specjalne_dodaj()

    if request.method == 'POST':
        if request.POST.get('konto'):
            konto = request.POST.get('konto')
            tytul = request.POST.get('tytul')
            konto_wn = request.POST.get('konto_wn')
            konto_ma = request.POST.get('konto_ma')

            if fp.dodaj_konto_specjalne(konto, tytul, konto_wn, konto_ma):
                alert_message = fp.alert_message('DODANO NOWE KONTO SPECJALNE')
            else:
                alert_message = fp.alert_message(alert = 'error',  info = f'KONTO {konto} JUŻ ISTNIEJE')
            tabela_konta_specjalne = generator_tabeli.tabela_konta_specjalne()

        elif request.POST.get('konto_specjalne_delete_nr'):
            konto = request.POST.get('konto_specjalne_delete_nr')
            fp.konto_specjalne_delete(konto)
            alert_message = fp.alert_message(f'KONTO SPECJALNE {konto} ZOSTAŁO SKASOWANE')

    tabela_konta_specjalne = generator_tabeli.tabela_konta_specjalne()

    return render(request, 'zpt_manager/sage_konta_specjalne.html',
                  {
                      'title': 'KONTA SPECJALNE',
                      'tabela_konta_specjalne': tabela_konta_specjalne,
                      'form_edycja_display': form_edycja_display,
                      'form_konto_specjalne_dodaj': form_konto_specjalne_dodaj,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('sage'),
                  })

def sage_kontrahenci_stali(request):
    alert_message = fp.alert_message()
    form_sagea_kontrahenci_stali = Form_sage_kontrahenci_stali()
    tabela_kontrahenci_stali = ''

    if request.method == 'POST':
        if request.POST.get('kontrahenci_stali_import_danych'):
            fp.kontrahenci_stali_import_danych()
            alert_message = fp.alert_message('DANE ZOSTAŁY ZAIMPORTOWANE')

        elif request.POST.get('nazwa'):
            nazwa = request.POST.get('nazwa')
            tabela_kontrahenci_stali = generator_tabeli.tabela_kontrahenci_stali(rodzaj = 'nazwa', fraza=nazwa)
            pass #wybór po nazwie

        elif request.POST.get('nip'):
            nip = request.POST.get('nip')
            tabela_kontrahenci_stali = generator_tabeli.tabela_kontrahenci_stali(rodzaj='nip', fraza=nip)

        else:
            tabela_kontrahenci_stali = generator_tabeli.tabela_kontrahenci_stali(rodzaj='all', fraza='')




    return render(request, 'zpt_manager/sage_kontrahenci_stali.html',
                  {
                      'title': 'KONTRAHENCI STALI',
                      'tabela_kontrahenci_stali': tabela_kontrahenci_stali,
                      'form_sagea_kontrahenci_stali': form_sagea_kontrahenci_stali,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('sage'),
                  })

def sage_rf_pliki(request):
    alert_message = fp.alert_message()
    form_sage_rf_pliki = Form_sage_rf_pliki()
    form_sage_rf_pliki.fields['rok_miesiac'].initial = fp.sage_rf_pliki_set_miesiac()
    raport_eksportu = ''

    if request.method == 'POST':
        if request.POST.get('lista_aptek') == '1':
            alert_message = fp.alert_message(info='MUSISZ WYBRAĆ APTEKĘ', alert='error')
            raport_eksportu = 'Błąd'
        else:
            raport_eksportu = fp.sage_rf_pliki_eksport(request.POST.get('lista_aptek'), request.POST.get('rok_miesiac'))

    return render(request, 'zpt_manager/sage_rf_pliki.html',
                  {
                      'title': 'SAGE RF',
                      'raport_eksportu': raport_eksportu,
                      'form_sage_rf_pliki': form_sage_rf_pliki,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('sage'),
                  })


def testy_rozne(request):

    test_form = Form_Testy()
    if request.method == 'POST':
        alert_message = ""
    else:
        alert_message = ''
    return render(request, 'zpt_manager/testy_rozne.html',
                  {
                      'test_form': test_form,
                      'alert_message': alert_message,
                      'footer_data': fp.footer_data(),
                      'active_link': fp.active_link_navbar('testy'),
                  })

