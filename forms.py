from django import forms
import datetime
from . import slowniki
from . import funkcje_pomocnicze as fp
from dal import autocomplete


class Gotowka_Form(forms.Form):
    lista_gotowki = forms.ChoiceField(choices=slowniki.gotowki,
                                      widget = forms.Select(attrs={'onchange': 'this.form.submit();',
                                                                   'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')

class Gotowka_Form_dodaj(forms.Form):
    data_gotowki_dodaj = forms.DateField(label= '',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                                 'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                                 }))
    apteka_gotowki_dodaj = forms.ChoiceField(choices=slowniki.gotowki_dodaj,
                               widget = forms.Select(attrs={'class': 'form-control',
                                                                    'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;'}),
                                      label='')
    # kwota = forms.IntegerField(widget = forms.NumberInput(attrs={'class': 'form-control'}))
    kwota_gotowki_dodaj = forms.IntegerField(required=True, widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white; background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'KWOTA'}))
    opis_gotowki_dodaj = forms.CharField(required=False, label='', max_length = 100,
                                         widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'OPIS'}))

class Gotowka_Form_edytuj(forms.Form):
    data_gotowki_edutuj = forms.DateField(label= '',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                                 'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',

                                                                 }))
    apteka_gotowki_edutuj = forms.ChoiceField(choices=slowniki.gotowki_dodaj,
                               widget = forms.Select(attrs={'class': 'form-control',
                                                                    'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;'}),
                                      label='')
    # kwota = forms.IntegerField(widget = forms.NumberInput(attrs={'class': 'form-control'}))
    kwota_gotowki_edutuj = forms.IntegerField(required=True, widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white; background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'KWOTA'}))
    opis_gotowki_edutuj = forms.CharField(required=False, label='', max_length = 100,
                                         widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'OPIS'}))

class Koszty_Form_Faktury_dodaj(forms.Form):
    # kod do listy wyboru
    lista_kontrahentow = fp.get_lista_kontrahentow_koszty()
    koszty_faktury_kontrahent = forms.ChoiceField(choices=lista_kontrahentow,
                               widget = forms.Select(attrs={'class': 'form-control',
                                                                    'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;'}),
                                      label='')

    #kod do datalist
    # koszty_faktury_kontrahent = forms.CharField(required=True, label='',
    #                                               widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                                             'list': 'koszty_faktury_kontrahent',
    #                                                              'style': 'color: white;'
    #                                                                       ' background-color: #8a8a8a;'
    #                                                                       'font-size: 12px;',
    #                                                            'placeholder': 'KONTRAHENT'}))


    koszty_faktury_faktura = forms.CharField(required=True, label='', max_length = 100,
                                         widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'FAKTURA'}))
    koszty_faktury_kwota = forms.FloatField(required=True, label='',
                                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'style': 'color: white;'
                                                                                    ' background-color: #8a8a8a;'
                                                                                    'font-size: 12px;',
                                                                           'placeholder': 'KWOTA'}))
    koszty_faktury_data = forms.DateField(label= '',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                                 'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',

                                                                 }))

class Koszty_Form_Faktury_edytuj(forms.Form):
    # kod do listy wyboru
    lista_kontrahentow = fp.get_lista_kontrahentow_koszty()
    koszty_faktury_kontrahent_edytuj = forms.ChoiceField(choices=lista_kontrahentow,
                               widget = forms.Select(attrs={'class': 'form-control',
                                                                    'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;'}),
                                      label='')

    koszty_faktury_faktura_edytuj = forms.CharField(required=True, label='', max_length = 100,
                                         widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'FAKTURA'}))
    koszty_faktury_kwota_edytuj = forms.FloatField(required=True, label='',
                                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'style': 'color: white;'
                                                                                    ' background-color: #8a8a8a;'
                                                                                    'font-size: 12px;',
                                                                           'placeholder': 'KWOTA'}))
    koszty_faktury_data_edytuj = forms.DateField(label= '',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                                 'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',

                                                                 }))

class Koszty_Form_Kontrahenci_dodaj(forms.Form):
    koszty_kontr_nazwa_dodaj = forms.CharField(required=True, label='', max_length=100,
                                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                  'style': 'color: white;'
                                                                                           ' background-color: #8a8a8a;'
                                                                                           'font-size: 12px;',
                                                                                  'placeholder': 'NAZWA'}))
    koszty_kontr_nip_dodaj = forms.CharField(required=True, label='', max_length=100,
                                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'style': 'color: white;'
                                                                                      ' background-color: #8a8a8a;'
                                                                                      'font-size: 12px;',
                                                                             'placeholder': 'NIP'}))
    koszty_kontr_konto_dodaj = forms.CharField(required=True, label='', max_length=100,
                                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'style': 'color: white;'
                                                                                      ' background-color: #8a8a8a;'
                                                                                      'font-size: 12px;',
                                                                             'placeholder': 'KONTO'}))

class Koszty_Form_Kontrahenci_edytuj(forms.Form):
    koszty_kontr_nazwa_edytuj = forms.CharField(required=True, label='', max_length=100,
                                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'style': 'color: white;'
                                                                                      ' background-color: #8a8a8a;'
                                                                                      'font-size: 12px;',
                                                                             'placeholder': 'NAZWA'}))
    koszty_kontr_nip_edytuj = forms.CharField(required=True, label='', max_length=100,
                                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'style': 'color: white;'
                                                                                    ' background-color: #8a8a8a;'
                                                                                    'font-size: 12px;',
                                                                           'placeholder': 'NIP'}))
    koszty_kontr_konto_edytuj = forms.CharField(required=True, label='', max_length=100,
                                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'style': 'color: white;'
                                                                                      ' background-color: #8a8a8a;'
                                                                                      'font-size: 12px;',
                                                                             'placeholder': 'KONTO'}))

class Faktury_Form_wyszukaj(forms.Form):
    numer_faktury = forms.CharField(required=True, label='', max_length=100, min_length=5,
                                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'style': 'color: white;'
                                                                                       ' background-color: #8a8a8a;'
                                                                                       'font-size: 12px;',
                                                                              'placeholder': 'NUMER FAKTURY'}))

class Form_Faktury_Wykaz_Dostawca(forms.Form):
    dostawca = forms.ChoiceField(choices=fp.faktury_wykaz_get_dostawcy(),
                                      widget = forms.Select(attrs={'onchange': 'this.form.submit();',
                                                                   'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')

class Form_Faktury_Wykaz_Kontrahent(forms.Form):
    kontrahent = forms.ChoiceField(choices=fp.faktury_wykaz_get_kontrahenci(),
                                      widget = forms.Select(attrs={'onchange': 'this.form.submit();',
                                                                   'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')

class Towar_Dostawcy_Form_dodaj(forms.Form):
    towar_dostawcy_nazwa_dodaj = forms.CharField(required=True, label='', max_length=100,
                                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'style': 'color: white;'
                                                                                      ' background-color: #8a8a8a;'
                                                                                      'font-size: 12px;',
                                                                             'placeholder': 'NAZWA'}))
    towar_dostawcy_nip_dodaj = forms.CharField(required=True, label='', max_length=15,
                                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'style': 'color: white;'
                                                                                  ' background-color: #8a8a8a;'
                                                                                  'font-size: 12px;',
                                                                         'placeholder': 'NIP'}))
    towar_dostawcy_konto_dodaj = forms.CharField(required=True, label='', max_length=50,
                                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'style': 'color: white;'
                                                                                  ' background-color: #8a8a8a;'
                                                                                  'font-size: 12px;',
                                                                         'placeholder': 'KONTO'}))
    towar_dostawcy_id_02_dodaj = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 02'}))
    towar_dostawcy_id_03_dodaj = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 03'}))
    towar_dostawcy_id_04_dodaj = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 04'}))
    towar_dostawcy_id_05_dodaj = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 05'}))
    towar_dostawcy_id_06_dodaj = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 06'}))
    towar_dostawcy_id_07_dodaj = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 07'}))
    towar_dostawcy_id_08_dodaj = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 08'}))

class Towar_Dostawcy_Form_edycja(forms.Form):
    towar_dostawcy_nazwa_edycja = forms.CharField(required=True, label='', max_length=100,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'NAZWA'}))
    towar_dostawcy_nip_edycja = forms.CharField(required=True, label='', max_length=15,
                                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'style': 'color: white;'
                                                                                      ' background-color: #8a8a8a;'
                                                                                      'font-size: 12px;',
                                                                             'placeholder': 'NIP'}))
    towar_dostawcy_konto_edycja = forms.CharField(required=True, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'KONTO'}))
    towar_dostawcy_id_02_edycja = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 02'}))
    towar_dostawcy_id_03_edycja = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 03'}))
    towar_dostawcy_id_04_edycja = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 04'}))
    towar_dostawcy_id_05_edycja = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 05'}))
    towar_dostawcy_id_06_edycja = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 06'}))
    towar_dostawcy_id_07_edycja = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 07'}))
    towar_dostawcy_id_08_edycja = forms.CharField(required=False, label='', max_length=50,
                                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'style': 'color: white;'
                                                                                        ' background-color: #8a8a8a;'
                                                                                        'font-size: 12px;',
                                                                               'placeholder': 'ID: 08'}))

class Hurtownie_Import_Danych(forms.Form):
    hurtownia = forms.ChoiceField(choices=slowniki.hurtownie_import,
                               widget = forms.Select(attrs={'class': 'form-control',
                                                                    'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;'}),
                                      label='')
    plik = forms.FileField(widget= forms.FileInput(attrs={'class': 'form-control',
                                                                    'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;'}))

class Hurtownie_Faktury(forms.Form):
    hurtownia = forms.ChoiceField(choices=slowniki.hurtownie_import,
                               widget = forms.Select(attrs={'onchange': 'this.form.submit();',
                                                            'class': 'form-control',
                                                                    'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;'}),
                                      label='')

    data = forms.DateField(label='',
                                         initial=datetime.date.today(),
                                         widget=forms.DateInput(attrs={'onchange': 'this.form.submit();',
                                                                       'type': 'date',
                                                                       'class': 'form-control',
                                                                       'style': 'color: white;'
                                                                                ' background-color: #8a8a8a;'
                                                                                'font-size: 12px;',

                                                                       }))

class Hurtownie_Zestawienia(forms.Form):
    hurtownia = forms.ChoiceField(choices=slowniki.hurtownie_import,
                               widget = forms.Select(attrs={'onchange': 'this.form.submit();',
                                                            'class': 'form-control',
                                                                    'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;'}),
                                      label='')

class Przelewy_Szukaj_Form(forms.Form):
    tytul_przelwu = forms.CharField(required=False, label='', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;',
                                                                  'placeholder': 'TYTUŁ PRZELEWU'}))

    odbiorca_przelwu = forms.CharField(required=False, label='', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;',
                                                                  'placeholder': 'ODBIORCA PRZELEWU'}))

class Pracownicy_Dane_Form(forms.Form):
    lista_pracownikow = forms.ChoiceField(choices=sorted(slowniki.pracownicy_dane_wybor,key=lambda x: x[1]),
                                      widget = forms.Select(attrs={'onchange': 'this.form.submit();',
                                                                   'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')

class Pracownicy_Dane_Edycja_Form(forms.Form):
    imie = forms.CharField(required=False, label='', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    nazwisko = forms.CharField(required=False, label='', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    pensja = forms.CharField(required=False, label='PENSJA', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    badania = forms.CharField(required=False, label='BADANIA', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    data_zakonczenia_umowy = forms.CharField(required=False, label='DATA ZAKOŃCZENIA UMOWY', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    konto_bankowe = forms.CharField(required=False, label='KONTO BANKOWE', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    stanowisko = forms.CharField(required=False, label='STANOWISKO', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    placowka = forms.CharField(required=False, label='PLACOWKA', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    aktywny = forms.ChoiceField(choices=(('0','TAK'),('1','NIE')),
                                      widget = forms.Select(attrs={'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')
    pranie = forms.CharField(required=False, label='PRANIE', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    premia = forms.CharField(required=False, label='PREMIA', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    uwagi_wynagrodzenia = forms.CharField(required=False, label='UWAGI DO WYNAGRODZENIA', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))
    data_urodzenia = forms.CharField(required=False, label='DATA URODZENIA', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;'}))

class Pracownicy_Nieobecnosci_dodaj_Form(forms.Form):
    rodzaj_nieobecnosci = forms.ChoiceField(choices=slowniki.rodzaj_nieobecnosci_tuple,
                                      widget = forms.Select(attrs={'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')

    data_nieobecnosci_od = forms.DateField(label='',
                                         initial=datetime.date.today,
                                         widget=forms.TextInput(attrs={'type': 'date',
                                                                       'class': 'form-control',
                                                                       'style': 'color: white;'
                                                                                ' background-color: #8a8a8a;'
                                                                                'font-size: 12px;',
                                                                       }))

    data_nieobecnosci_do = forms.DateField(label='',
                                           initial=datetime.date.today,
                                           widget=forms.TextInput(attrs={'type': 'date',
                                                                         'class': 'form-control',
                                                                         'style': 'color: white;'
                                                                                  ' background-color: #8a8a8a;'
                                                                                  'font-size: 12px;',
                                                                         }))

    uwagi = forms.CharField(required=False, label='', max_length=100,
                                       widget=forms.TextInput(attrs={'class': 'form-control',
                                                                     'style': 'color: white;'
                                                                              ' background-color: #8a8a8a;'
                                                                              'font-size: 12px;',
                                                                     'placeholder': 'UWAGI'}))

class Rozne_fundusze_l_dodaj(forms.Form):
    data = forms.DateField(label= '',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                                 'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                                 }))
    kwota = forms.IntegerField(required=True, widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white; background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'KWOTA'}))
    opis = forms.CharField(required=False, label='', max_length = 100,
                                         widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'OPIS'}))

class Rozne_fundusze_l_edycja(forms.Form):
    data_edycja = forms.DateField(label= '',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                                 'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                                 }))
    kwota_edycja = forms.IntegerField(required=True, widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white; background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'KWOTA'}))
    opis_edycja = forms.CharField(required=False, label='', max_length = 100,
                                         widget = forms.TextInput(attrs={'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                               'placeholder': 'OPIS'}))

class Rozne_karty_hallera_form(forms.Form):
    data = forms.DateField(label='',
                                  initial=datetime.date.today,
                                  widget=forms.TextInput(attrs={'type': 'date',
                                                                'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;',
                                                                }))
    kwota = forms.FloatField(required=True, label='',
                                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'style': 'color: white;'
                                                                                    ' background-color: #8a8a8a;'
                                                                                    'font-size: 12px;',
                                                                           'placeholder': 'KWOTA'}))

class Rozne_czynsze(forms.Form):
    data = forms.DateField(label='',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                         'class': 'form-control',
                                                         'style': 'color: white;'
                                                                  ' background-color: #8a8a8a;'
                                                                  'font-size: 12px;',
                                                         }))
    nr_rachunku = forms.CharField(required=False, label='', max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px; text-align: center;',
                                                                'placeholder': 'NR RACHUNKU'}))

    kontrahent = forms.ChoiceField(choices=slowniki.czynsze_kontrahenci_tuple,
                                      widget = forms.Select(attrs={'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')

    pole_1 = forms.CharField(required=False, label='', max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;',
                                                                'placeholder': 'OPIS'}))

    pole_2 = forms.CharField(required=False, label='', max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;',
                                                                'placeholder': 'OPIS'}))

    pole_3 = forms.CharField(required=False, label='', max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;',
                                                                'placeholder': 'OPIS'}))

    pole_4 = forms.CharField(required=False, label='', max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;',
                                                                'placeholder': 'OPIS'}))

    pole_5 = forms.CharField(required=False, label='', max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;',
                                                                'placeholder': 'OPIS'}))

    kwota_1 = forms.FloatField(required=True, label='',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;',
                                                           'placeholder': 'KWOTA', 'id': 'kwota_1'}))

    kwota_2 = forms.FloatField(required=True, label='',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;',
                                                           'placeholder': 'KWOTA', 'id': 'kwota_2'}))

    kwota_3 = forms.FloatField(required=True, label='',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;',
                                                           'placeholder': 'KWOTA', 'id': 'kwota_3'}))

    kwota_4 = forms.FloatField(required=True, label='',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;',
                                                           'placeholder': 'KWOTA', 'id': 'kwota_4'}))

    kwota_5 = forms.FloatField(required=True, label='',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;',
                                                           'placeholder': 'KWOTA', 'id': 'kwota_5'}))

    suma = forms.FloatField(required=True, label='',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'style': 'color: white;'
                                                                      ' background-color: #8a8a8a;'
                                                                      'font-size: 12px;',
                                                             'placeholder': 'SUMA', 'id': 'suma'}))

    licznik_teraz = forms.FloatField(required=True, label='',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'style': 'color: white;'
                                                                      ' background-color: #8a8a8a;'
                                                                      'font-size: 12px;',
                                                             'placeholder': 'LICZNIK'}))

    licznik_ostatni = forms.FloatField(required=True, label='',
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'style': 'color: white;'
                                                                            ' background-color: #8a8a8a;'
                                                                            'font-size: 12px;',
                                                                   'placeholder': 'LICZNIK'}))

    stawka_kWh = forms.FloatField(required=True, label='',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'style': 'color: white;'
                                                                      ' background-color: #8a8a8a;'
                                                                      'font-size: 12px;',
                                                             'placeholder': 'STAWKA'}))

class Rozne_biala_lista_wyszukaj(forms.Form):
    nazwa = forms.CharField(required=False, label='', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;',
                                                                  'placeholder': 'NAZWA PODMIOTU - WYSZUKAJ'}))

class Rozne_dyzury(forms.Form):
    data_start = forms.DateField(label='DATA START',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                         'class': 'form-control',
                                                         'style': 'color: white;'
                                                                  ' background-color: #8a8a8a;'
                                                                  'font-size: 12px;',
                                                         }))
    data_stop = forms.DateField(label='DATA STOP',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                         'class': 'form-control',
                                                         'style': 'color: white;'
                                                                  ' background-color: #8a8a8a;'
                                                                  'font-size: 12px;',
                                                         }))

class Form_reklamowiki(forms.Form):
    kwartal = forms.ChoiceField(choices=slowniki.rozne_reklamowiki_kwartal_wybor,
                                      widget = forms.Select(attrs={'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')

    rok = forms.CharField(required=True, initial= datetime.datetime.now().date().year, label='', max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px; text-align: center;',
                                                                'placeholder': 'ROK'}))

class Form_todo(forms.Form):
    data_dodania = forms.DateField(label='',
                           initial=datetime.date.today,
                           widget=forms.TextInput(attrs={'type': 'date',
                                                         'class': 'form-control',
                                                         'style': 'color: white;'
                                                                  ' background-color: #8a8a8a;'
                                                                  'font-size: 12px;',
                                                         }))

    termin = forms.DateField(label='',
                                   initial=datetime.date.today,
                                   widget=forms.TextInput(attrs={'type': 'date',
                                                                 'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                                 }))

    nazwa = forms.CharField(required=False, label='', max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;',
                                                                  'placeholder': 'TYTUŁ'}))

    opis = forms.CharField(required=False, label='',
                                    widget=forms.Textarea(attrs={'class': 'form-control',
                                                                  'style': 'color: black;'
                                                                           ' background-color: #8a8a8a;'
                                                                           'font-size: 12px;',
                                                                  'placeholder': 'TUTAJ WPISZ OPIS ZADNIA',
                                                                 'rows':20, 'cols':15}))

class Form_archiwum_daty(forms.Form):
    data_od = forms.DateField(label='',
                                   initial=datetime.date.today,
                                   widget=forms.TextInput(attrs={'type': 'date',
                                                                 'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                                 }))
    data_do = forms.DateField(label='',
                              initial=datetime.date.today,
                              widget=forms.TextInput(attrs={'type': 'date',
                                                            'class': 'form-control',
                                                            'style': 'color: white;'
                                                                     ' background-color: #8a8a8a;'
                                                                     'font-size: 12px;',
                                                            }))

class Form_sage_wyciag_millenium(forms.Form):
    wyciag_millenium_id = forms.ChoiceField(choices=(),
                                      widget = forms.Select(attrs={'onchange': 'this.form.submit();',
                                                                   'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')

class Form_sage_wyciag_pko(forms.Form):
    wyciag_pko_id = forms.ChoiceField(choices=(),
                                      widget = forms.Select(attrs={'onchange': 'this.form.submit();',
                                                                   'class': 'form-select',
                                                                   'style': 'color: white; background-color: #8a8a8a;'
                                                                            'font-size: 12px;'}),
                                      label='')

class Form_sage_import_wyciag(forms.Form):

    plik = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control',
                                                         'style': 'color: white;'
                                                                  ' background-color: #8a8a8a;'
                                                                  'font-size: 12px;'}))

class Form_sage_wyciag_edycja_pozycji(forms.Form):
    wyciag = forms.CharField(required=False, label = '', max_length = 100,
                                    widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control',
                                                                  'style': 'color: white;'
                                                                           ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;'}))

    nr_transakcji = forms.CharField(required=False, label='', max_length=100,
                             widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control',
                                                           'style': 'color: white;'
                                                                    ' background-color: #8a8a8a;'
                                                                    'font-size: 12px;'}))

    data = forms.DateField(label='', widget=forms.TextInput(attrs={'readonly': True, 'type': 'date',
                                                                 'class': 'form-control',
                                                                 'style': 'color: white;'
                                                                          ' background-color: #8a8a8a;'
                                                                          'font-size: 12px;',
                                                                 }))

    tytul = forms.CharField(required=False, label='', max_length=100,
                    widget=forms.TextInput(attrs={'readonly': False, 'class': 'form-control',
                                                  'style': 'color: white;'
                                                           ' background-color: #8a8a8a;'
                                                           'font-size: 12px;'}))

    kontrahent = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;'}))

    kwota = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;'}))

    nip = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;'}))

    konto_wn = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'readonly': False, 'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;'}))

    konto_ma = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'readonly': False, 'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;'}))

    id_sage = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;'}))

    rachunek = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;'}))

    konto_spec = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;'}))

    rodzaj = forms.CharField(required=False, label='', max_length=100,
                                 widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control',
                                                               'style': 'color: white;'
                                                                        ' background-color: #8a8a8a;'
                                                                        'font-size: 12px;'}))

class Form_sage_konta_specjalne_dodaj(forms.Form):
    konto = forms.CharField(required=True, label='', max_length=100,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'style': 'color: white;'
                                                                                ' background-color: #8a8a8a;'
                                                                                'font-size: 12px;',
                                                                       'placeholder': 'KONTO'}))
    tytul = forms.CharField(required=True, label='', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;',
                                                          'placeholder': 'TYTUŁ'}))
    konto_wn = forms.CharField(required=True, label='', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;',
                                                          'placeholder': 'KONTO WN'}))
    konto_ma = forms.CharField(required=True, label='', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;',
                                                          'placeholder': 'KONTO MA'}))

class Form_sage_kontrahenci_stali(forms.Form):
    nazwa = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;',
                                                          'placeholder': 'NAZWA'}))
    nip = forms.CharField(required=False, label='', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;',
                                                          'placeholder': 'NIP'}))

class Form_sage_rf_pliki(forms.Form):
    lista_aptek = forms.ChoiceField(choices=slowniki.sage_rf_plik_apteki,
                                      widget=forms.Select(attrs={'class': 'form-select',
                                                                 'style': 'color: white; background-color: #8a8a8a;'
                                                                          'font-size: 12px;'}),
                                      label='')
    rok_miesiac = forms.CharField(required=True, label='', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'style': 'color: white;'
                                                                   ' background-color: #8a8a8a;'
                                                                   'font-size: 12px;',
                                                          'placeholder': 'ROK-MIESIĄC'}))


class Form_Testy(forms.Form):
    pole_1 = forms.FloatField(required=True, label='',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;',
                                                                'placeholder': 'STAWKA', 'id': 'pole_1'}))
    pole_2 = forms.FloatField(required=True, label='',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;',
                                                                'placeholder': 'STAWKA', 'id': 'pole_2'}))
    pole_3 = forms.FloatField(required=True, label='',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'style': 'color: white;'
                                                                         ' background-color: #8a8a8a;'
                                                                         'font-size: 12px;',
                                                                'placeholder': 'STAWKA', 'id': 'pole_3'}))



