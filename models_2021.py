# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Aktualizacja(models.Model):
    apteka = models.IntegerField()
    data = models.TextField()
    opis = models.TextField()

    class Meta:
        managed = False
        db_table = 'aktualizacja'


class Aktywnosci(models.Model):
    id_apteki = models.IntegerField()
    id_aktywnosci = models.IntegerField()
    czas_aktywnosci = models.TextField()

    def __str__(self):
        return str(self.id_apteki) + ' ' + self.czas_aktywnosci
    class Meta:
        managed = False
        db_table = 'aktywnosci'


class AsortymentPartner(models.Model):
    apteka = models.IntegerField()
    miesiac = models.TextField()
    dane = models.TextField()
    bloz_nazwa = models.TextField()

    class Meta:
        managed = False
        db_table = 'asortyment_partner'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Backup(models.Model):
    apteka = models.IntegerField()
    czas_start = models.TextField()
    plik_stop = models.TextField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'backup'


class BialaLista(models.Model):
    czas = models.TextField()
    nazwa = models.TextField()
    konto = models.TextField()
    nip = models.TextField()
    status = models.TextField()
    kod_potw = models.TextField()

    class Meta:
        managed = False
        db_table = 'biala_lista'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Dostawcy(models.Model):
    nazwa = models.TextField()
    id_02 = models.IntegerField()
    id_03 = models.IntegerField()
    id_04 = models.IntegerField()
    id_05 = models.IntegerField()
    id_06 = models.IntegerField()
    id_07 = models.IntegerField()
    id_08 = models.IntegerField()
    nip = models.TextField()
    konto = models.TextField()

    class Meta:
        managed = False
        db_table = 'dostawcy'


class FvSage(models.Model):
    apteka = models.IntegerField()
    data_akt = models.TextField()
    dane = models.TextField()

    class Meta:
        managed = False
        db_table = 'fv_sage'


class Gotowki(models.Model):
    id_got = models.AutoField(primary_key=True)
    data = models.TextField()
    id_apteka = models.IntegerField()
    kwota = models.IntegerField()
    opis = models.TextField()

    class Meta:
        managed = False
        db_table = 'gotowki'


class GotowkiXx(models.Model):
    data = models.TextField()
    opis = models.TextField()
    kwota = models.TextField()

    class Meta:
        managed = False
        db_table = 'gotowki_xx'


class GrupyTowarowe(models.Model):
    id_grupy = models.IntegerField(db_column='ID_grupy', blank=True, null=True)  # Field name made lowercase.
    nazwa_grupy = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    nazwa = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupy_towarowe'


class GrupyTowaroweSprzedazFwd(models.Model):
    bloz = models.TextField(db_column='BLOZ', blank=True, null=True)  # Field name made lowercase.
    sprzedaz = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupy_towarowe_sprzedaz_fwd'


class GrupyZakupoweId(models.Model):
    id_grupy = models.IntegerField()
    nazwa = models.TextField()

    class Meta:
        managed = False
        db_table = 'grupy_zakupowe_id'


class IdAktywnosci(models.Model):
    id_akt = models.AutoField(primary_key=True)
    nazwa_akt = models.TextField()

    class Meta:
        managed = False
        db_table = 'id_aktywnosci'


class IdNazwaBloz02(models.Model):
    id_towr = models.IntegerField(primary_key=True)
    nazwa = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    nrtow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'id_nazwa_bloz_02'


class IdNazwaBloz03(models.Model):
    id_towr = models.IntegerField(primary_key=True)
    nazwa = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    nrtow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'id_nazwa_bloz_03'


class IdNazwaBloz04(models.Model):
    id_towr = models.IntegerField(primary_key=True)
    nazwa = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    nrtow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'id_nazwa_bloz_04'


class IdNazwaBloz05(models.Model):
    id_towr = models.IntegerField(primary_key=True)
    nazwa = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    nrtow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'id_nazwa_bloz_05'


class IdNazwaBloz06(models.Model):
    id_towr = models.IntegerField(primary_key=True)
    nazwa = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    nrtow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'id_nazwa_bloz_06'


class IdNazwaBloz07(models.Model):
    id_towr = models.IntegerField(primary_key=True)
    nazwa = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    nrtow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'id_nazwa_bloz_07'


class IdNazwaBloz08(models.Model):
    id_towr = models.IntegerField(primary_key=True)
    nazwa = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    nrtow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'id_nazwa_bloz_08'


class JednostkiOrg(models.Model):
    id_jednostki = models.AutoField(primary_key=True)
    nazwa = models.TextField(db_collation='utf8_polish_ci')
    id_02 = models.IntegerField()
    id_03 = models.IntegerField()
    id_04 = models.IntegerField()
    id_05 = models.IntegerField()
    id_06 = models.IntegerField()
    id_07 = models.IntegerField()
    id_08 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'jednostki_org'


class KrotkieDatySprzedaz(models.Model):
    bloz = models.IntegerField(db_column='BLOZ', primary_key=True)  # Field name made lowercase.
    s02 = models.TextField(blank=True, null=True)
    s03 = models.TextField(blank=True, null=True)
    s04 = models.TextField(blank=True, null=True)
    s05 = models.TextField(blank=True, null=True)
    s06 = models.TextField(blank=True, null=True)
    s07 = models.TextField(blank=True, null=True)
    s08 = models.TextField(blank=True, null=True)
    st02 = models.TextField(blank=True, null=True)
    st03 = models.TextField(blank=True, null=True)
    st04 = models.TextField(blank=True, null=True)
    st05 = models.TextField(blank=True, null=True)
    st06 = models.TextField(blank=True, null=True)
    st07 = models.TextField(blank=True, null=True)
    st08 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'krotkie_daty_sprzedaz'


class Logowanie(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user = models.TextField()
    data_log = models.TextField()
    ip_log = models.TextField()

    class Meta:
        managed = False
        db_table = 'logowanie'


class Monitor(models.Model):
    apteka = models.IntegerField()
    godzina = models.TextField()

    class Meta:
        managed = False
        db_table = 'monitor'


class NewRem04(models.Model):
    id_kzak = models.IntegerField(unique=True)
    id_dokf = models.TextField()
    id_towr = models.TextField()
    id_dost = models.TextField()
    bloz = models.TextField(blank=True, null=True)
    ilakt = models.TextField(blank=True, null=True)
    cena_zak = models.TextField(blank=True, null=True)
    dataw = models.TextField(blank=True, null=True)
    seria = models.TextField(blank=True, null=True)
    jednostka = models.TextField()
    datazak = models.TextField()
    dgakt = models.TextField(blank=True, null=True)
    empty = models.IntegerField(blank=True, null=True)
    nazwa = models.TextField(blank=True, null=True)
    cena_detal = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_rem_04'


class NewZamowienia02(models.Model):
    id_zam = models.IntegerField(unique=True)
    id_zam_zpt = models.IntegerField()
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'new_zamowienia_02'


class NewZamowienia03(models.Model):
    id_zam = models.IntegerField(unique=True)
    id_zam_zpt = models.IntegerField()
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'new_zamowienia_03'


class NewZamowienia04(models.Model):
    id_zam = models.IntegerField(unique=True)
    id_zam_zpt = models.IntegerField()
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'new_zamowienia_04'


class NewZamowienia05(models.Model):
    id_zam = models.IntegerField(unique=True)
    id_zam_zpt = models.IntegerField()
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'new_zamowienia_05'


class NewZamowienia06(models.Model):
    id_zam = models.IntegerField(unique=True)
    id_zam_zpt = models.IntegerField()
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'new_zamowienia_06'


class NewZamowienia07(models.Model):
    id_zam = models.IntegerField(unique=True)
    id_zam_zpt = models.IntegerField()
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'new_zamowienia_07'


class NewZamowienia08(models.Model):
    id_zam = models.IntegerField(unique=True)
    id_zam_zpt = models.IntegerField()
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'new_zamowienia_08'


class NewZamowieniaGodziny(models.Model):
    apteka = models.IntegerField()
    data_klik = models.TextField()
    godzina_klik = models.TextField()
    id_zam = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'new_zamowienia_godziny'


class NewZwroty02(models.Model):
    nazwa = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.TextField(blank=True, null=True)
    ilosc = models.IntegerField(blank=True, null=True)
    data_zwrot = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_zwroty_02'


class NewZwroty03(models.Model):
    nazwa = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.TextField(blank=True, null=True)
    ilosc = models.IntegerField(blank=True, null=True)
    data_zwrot = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_zwroty_03'


class NewZwroty04(models.Model):
    nazwa = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.TextField(blank=True, null=True)
    ilosc = models.IntegerField(blank=True, null=True)
    data_zwrot = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_zwroty_04'


class NewZwroty05(models.Model):
    nazwa = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.TextField(blank=True, null=True)
    ilosc = models.IntegerField(blank=True, null=True)
    data_zwrot = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_zwroty_05'


class NewZwroty06(models.Model):
    nazwa = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.TextField(blank=True, null=True)
    ilosc = models.IntegerField(blank=True, null=True)
    data_zwrot = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_zwroty_06'


class NewZwroty07(models.Model):
    nazwa = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.TextField(blank=True, null=True)
    ilosc = models.IntegerField(blank=True, null=True)
    data_zwrot = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_zwroty_07'


class NewZwroty08(models.Model):
    nazwa = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.TextField(blank=True, null=True)
    ilosc = models.IntegerField(blank=True, null=True)
    data_zwrot = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_zwroty_08'


class ObrotyDzienne(models.Model):
    data = models.TextField()
    apteka = models.IntegerField()
    pacjenci = models.IntegerField()
    obrot_brutto = models.FloatField()
    obrot_netto = models.FloatField()
    zysk_netto = models.FloatField()
    czas = models.IntegerField()

    class Meta:
        db_table = 'obroty_dzienne'
        unique_together = (('apteka', 'data'),)


class OperacjeBezgotowkowe02(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_rpks = models.IntegerField(db_column='ID_RPKS')  # Field name made lowercase.
    apteka_plus = models.TextField()
    data_wpis = models.TextField()
    godz_wpis = models.TextField()
    kwota_minus = models.FloatField()
    nr_dowodu_minus = models.TextField()
    kwota_plus = models.FloatField()
    uwagi = models.TextField()
    nr_dow_plus = models.TextField()
    potwierdzenie = models.IntegerField()
    data_potw = models.TextField()
    potw_system = models.IntegerField()
    dgakt = models.TextField()
    apteka_mail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'operacje_bezgotowkowe_02'


class OperacjeBezgotowkowe03(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_rpks = models.IntegerField(db_column='ID_RPKS')  # Field name made lowercase.
    apteka_plus = models.TextField()
    data_wpis = models.TextField()
    godz_wpis = models.TextField()
    kwota_minus = models.FloatField()
    nr_dowodu_minus = models.TextField()
    kwota_plus = models.FloatField()
    uwagi = models.TextField()
    nr_dow_plus = models.TextField()
    potwierdzenie = models.IntegerField()
    data_potw = models.TextField()
    potw_system = models.IntegerField()
    dgakt = models.TextField()
    apteka_mail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'operacje_bezgotowkowe_03'


class OperacjeBezgotowkowe04(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_rpks = models.IntegerField(db_column='ID_RPKS')  # Field name made lowercase.
    apteka_plus = models.TextField()
    data_wpis = models.TextField()
    godz_wpis = models.TextField()
    kwota_minus = models.FloatField()
    nr_dowodu_minus = models.TextField()
    kwota_plus = models.FloatField()
    uwagi = models.TextField()
    nr_dow_plus = models.TextField()
    potwierdzenie = models.IntegerField()
    data_potw = models.TextField()
    potw_system = models.IntegerField()
    dgakt = models.TextField()
    apteka_mail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'operacje_bezgotowkowe_04'


class OperacjeBezgotowkowe05(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_rpks = models.IntegerField(db_column='ID_RPKS')  # Field name made lowercase.
    apteka_plus = models.TextField()
    data_wpis = models.TextField()
    godz_wpis = models.TextField()
    kwota_minus = models.FloatField()
    nr_dowodu_minus = models.TextField()
    kwota_plus = models.FloatField()
    uwagi = models.TextField()
    nr_dow_plus = models.TextField()
    potwierdzenie = models.IntegerField()
    data_potw = models.TextField()
    potw_system = models.IntegerField()
    dgakt = models.TextField()
    apteka_mail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'operacje_bezgotowkowe_05'


class OperacjeBezgotowkowe06(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_rpks = models.IntegerField(db_column='ID_RPKS')  # Field name made lowercase.
    apteka_plus = models.TextField()
    data_wpis = models.TextField()
    godz_wpis = models.TextField()
    kwota_minus = models.FloatField()
    nr_dowodu_minus = models.TextField()
    kwota_plus = models.FloatField()
    uwagi = models.TextField()
    nr_dow_plus = models.TextField()
    potwierdzenie = models.IntegerField()
    data_potw = models.TextField()
    potw_system = models.IntegerField()
    dgakt = models.TextField()
    apteka_mail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'operacje_bezgotowkowe_06'


class OperacjeBezgotowkowe07(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_rpks = models.IntegerField(db_column='ID_RPKS')  # Field name made lowercase.
    apteka_plus = models.TextField()
    data_wpis = models.TextField()
    godz_wpis = models.TextField()
    kwota_minus = models.FloatField()
    nr_dowodu_minus = models.TextField()
    kwota_plus = models.FloatField()
    uwagi = models.TextField()
    nr_dow_plus = models.TextField()
    potwierdzenie = models.IntegerField()
    data_potw = models.TextField()
    potw_system = models.IntegerField()
    dgakt = models.TextField()
    apteka_mail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'operacje_bezgotowkowe_07'


class OperacjeBezgotowkowe08(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_rpks = models.IntegerField(db_column='ID_RPKS')  # Field name made lowercase.
    apteka_plus = models.TextField()
    data_wpis = models.TextField()
    godz_wpis = models.TextField()
    kwota_minus = models.FloatField()
    nr_dowodu_minus = models.TextField()
    kwota_plus = models.FloatField()
    uwagi = models.TextField()
    nr_dow_plus = models.TextField()
    potwierdzenie = models.IntegerField()
    data_potw = models.TextField()
    potw_system = models.IntegerField()
    dgakt = models.TextField()
    apteka_mail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'operacje_bezgotowkowe_08'


class PlatnosciFv(models.Model):
    id_fv = models.AutoField(primary_key=True)
    id_kont = models.IntegerField()
    nr_fv = models.TextField()
    kwota = models.TextField()
    data_platnosci = models.TextField()
    data_zaplaty = models.TextField()
    zaplacone = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'platnosci_fv'


class PlatnosciKontrahenci(models.Model):
    id_kont = models.AutoField(primary_key=True)
    nazwa = models.TextField()
    nip = models.TextField()
    konto = models.TextField()

    class Meta:
        managed = False
        db_table = 'platnosci_kontrahenci'


class PlatnosciTowar(models.Model):
    apteka = models.IntegerField(blank=True, null=True)
    dostawca = models.IntegerField(blank=True, null=True)
    nrfv = models.CharField(primary_key=True, max_length=30)
    data_zak = models.TextField(blank=True, null=True)
    data_platnosci = models.TextField(blank=True, null=True)
    kwota = models.FloatField(blank=True, null=True)
    zaplacone = models.IntegerField(blank=True, null=True)
    data_zaplaty = models.TextField(blank=True, null=True)
    dost_nazwa = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'platnosci_towar'


class Rem02(models.Model):
    id_kzak = models.IntegerField(unique=True)
    id_dokf = models.TextField()
    id_towr = models.TextField()
    id_dost = models.TextField()
    bloz = models.TextField(blank=True, null=True)
    ilakt = models.TextField(blank=True, null=True)
    cena_zak = models.TextField(blank=True, null=True)
    dataw = models.TextField(blank=True, null=True)
    seria = models.TextField(blank=True, null=True)
    jednostka = models.TextField()
    datazak = models.TextField()
    dgakt = models.TextField(blank=True, null=True)
    empty = models.IntegerField(blank=True, null=True)
    nazwa = models.TextField(blank=True, null=True)
    cena_detal = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rem_02'


class Rem03(models.Model):
    id_kzak = models.IntegerField(unique=True)
    id_dokf = models.TextField()
    id_towr = models.TextField()
    id_dost = models.TextField()
    bloz = models.TextField(blank=True, null=True)
    ilakt = models.TextField(blank=True, null=True)
    cena_zak = models.TextField(blank=True, null=True)
    dataw = models.TextField(blank=True, null=True)
    seria = models.TextField(blank=True, null=True)
    jednostka = models.TextField()
    datazak = models.TextField()
    dgakt = models.TextField(blank=True, null=True)
    empty = models.IntegerField(blank=True, null=True)
    nazwa = models.TextField(blank=True, null=True)
    cena_detal = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rem_03'


class Rem04(models.Model):
    id_kzak = models.IntegerField(unique=True)
    id_dokf = models.TextField()
    id_towr = models.TextField()
    id_dost = models.TextField()
    bloz = models.TextField(blank=True, null=True)
    ilakt = models.TextField(blank=True, null=True)
    cena_zak = models.TextField(blank=True, null=True)
    dataw = models.TextField(blank=True, null=True)
    seria = models.TextField(blank=True, null=True)
    jednostka = models.TextField()
    datazak = models.TextField()
    dgakt = models.TextField(blank=True, null=True)
    empty = models.IntegerField(blank=True, null=True)
    nazwa = models.TextField(blank=True, null=True)
    cena_detal = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rem_04'


class Rem05(models.Model):
    id_kzak = models.IntegerField(unique=True)
    id_dokf = models.TextField()
    id_towr = models.TextField()
    id_dost = models.TextField()
    bloz = models.TextField(blank=True, null=True)
    ilakt = models.TextField(blank=True, null=True)
    cena_zak = models.TextField(blank=True, null=True)
    dataw = models.TextField(blank=True, null=True)
    seria = models.TextField(blank=True, null=True)
    jednostka = models.TextField()
    datazak = models.TextField()
    dgakt = models.TextField(blank=True, null=True)
    empty = models.IntegerField(blank=True, null=True)
    nazwa = models.TextField(blank=True, null=True)
    cena_detal = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rem_05'


class Rem06(models.Model):
    id_kzak = models.IntegerField(unique=True)
    id_dokf = models.TextField()
    id_towr = models.TextField()
    id_dost = models.TextField()
    bloz = models.TextField(blank=True, null=True)
    ilakt = models.TextField(blank=True, null=True)
    cena_zak = models.TextField(blank=True, null=True)
    dataw = models.TextField(blank=True, null=True)
    seria = models.TextField(blank=True, null=True)
    jednostka = models.TextField()
    datazak = models.TextField()
    dgakt = models.TextField(blank=True, null=True)
    empty = models.IntegerField(blank=True, null=True)
    nazwa = models.TextField(blank=True, null=True)
    cena_detal = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rem_06'


class Rem07(models.Model):
    id_kzak = models.IntegerField(unique=True)
    id_dokf = models.TextField()
    id_towr = models.TextField()
    id_dost = models.TextField()
    bloz = models.TextField(blank=True, null=True)
    ilakt = models.TextField(blank=True, null=True)
    cena_zak = models.TextField(blank=True, null=True)
    dataw = models.TextField(blank=True, null=True)
    seria = models.TextField(blank=True, null=True)
    jednostka = models.TextField()
    datazak = models.TextField()
    dgakt = models.TextField(blank=True, null=True)
    empty = models.IntegerField(blank=True, null=True)
    nazwa = models.TextField(blank=True, null=True)
    cena_detal = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rem_07'


class Rem08(models.Model):
    id_kzak = models.IntegerField(unique=True)
    id_dokf = models.TextField()
    id_towr = models.TextField()
    id_dost = models.TextField()
    bloz = models.TextField(blank=True, null=True)
    ilakt = models.TextField(blank=True, null=True)
    cena_zak = models.TextField(blank=True, null=True)
    dataw = models.TextField(blank=True, null=True)
    seria = models.TextField(blank=True, null=True)
    jednostka = models.TextField()
    datazak = models.TextField()
    dgakt = models.TextField(blank=True, null=True)
    empty = models.IntegerField(blank=True, null=True)
    nazwa = models.TextField(blank=True, null=True)
    cena_detal = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rem_08'


class Saldo(models.Model):
    id_saldo = models.AutoField(primary_key=True)
    apteka = models.IntegerField()
    data = models.TextField()
    kwota = models.FloatField()
    opis = models.TextField()

    class Meta:
        managed = False
        db_table = 'saldo'


class Sprzedaz02(models.Model):
    id_sprz = models.IntegerField(primary_key=True)
    id_kzak = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    id_parag = models.IntegerField(blank=True, null=True)
    idtowr = models.TextField(blank=True, null=True)
    datsp = models.TextField(blank=True, null=True)
    ilosp = models.FloatField(blank=True, null=True)
    cenad = models.FloatField(blank=True, null=True)
    cenaz = models.FloatField(blank=True, null=True)
    vatsp = models.IntegerField(blank=True, null=True)
    cendn = models.FloatField(blank=True, null=True)
    gdzsp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sprzedaz_02'


class Sprzedaz03(models.Model):
    id_sprz = models.IntegerField(primary_key=True)
    id_kzak = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    id_parag = models.TextField(blank=True, null=True)
    idtowr = models.TextField(blank=True, null=True)
    datsp = models.TextField(blank=True, null=True)
    ilosp = models.FloatField(blank=True, null=True)
    cenad = models.FloatField(blank=True, null=True)
    cenaz = models.FloatField(blank=True, null=True)
    vatsp = models.IntegerField(blank=True, null=True)
    cendn = models.FloatField(blank=True, null=True)
    gdzsp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sprzedaz_03'


class Sprzedaz04(models.Model):
    id_sprz = models.IntegerField(primary_key=True)
    id_kzak = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    id_parag = models.TextField(blank=True, null=True)
    idtowr = models.TextField(blank=True, null=True)
    datsp = models.TextField(blank=True, null=True)
    ilosp = models.FloatField(blank=True, null=True)
    cenad = models.FloatField(blank=True, null=True)
    cenaz = models.FloatField(blank=True, null=True)
    vatsp = models.IntegerField(blank=True, null=True)
    cendn = models.FloatField(blank=True, null=True)
    gdzsp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sprzedaz_04'


class Sprzedaz05(models.Model):
    id_sprz = models.IntegerField(primary_key=True)
    id_kzak = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    id_parag = models.IntegerField(blank=True, null=True)
    idtowr = models.TextField(blank=True, null=True)
    datsp = models.TextField(blank=True, null=True)
    ilosp = models.FloatField(blank=True, null=True)
    cenad = models.FloatField(blank=True, null=True)
    cenaz = models.FloatField(blank=True, null=True)
    vatsp = models.IntegerField(blank=True, null=True)
    cendn = models.FloatField(blank=True, null=True)
    gdzsp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sprzedaz_05'


class Sprzedaz06(models.Model):
    id_sprz = models.IntegerField(primary_key=True)
    id_kzak = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    id_parag = models.IntegerField(blank=True, null=True)
    idtowr = models.TextField(blank=True, null=True)
    datsp = models.TextField(blank=True, null=True)
    ilosp = models.FloatField(blank=True, null=True)
    cenad = models.FloatField(blank=True, null=True)
    cenaz = models.FloatField(blank=True, null=True)
    vatsp = models.IntegerField(blank=True, null=True)
    cendn = models.FloatField(blank=True, null=True)
    gdzsp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sprzedaz_06'


class Sprzedaz07(models.Model):
    id_sprz = models.IntegerField(primary_key=True)
    id_kzak = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    id_parag = models.IntegerField(blank=True, null=True)
    idtowr = models.TextField(blank=True, null=True)
    datsp = models.TextField(blank=True, null=True)
    ilosp = models.FloatField(blank=True, null=True)
    cenad = models.FloatField(blank=True, null=True)
    cenaz = models.FloatField(blank=True, null=True)
    vatsp = models.IntegerField(blank=True, null=True)
    cendn = models.FloatField(blank=True, null=True)
    gdzsp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sprzedaz_07'


class Sprzedaz08(models.Model):
    id_sprz = models.IntegerField(primary_key=True)
    id_kzak = models.TextField(blank=True, null=True)
    bloz = models.TextField(blank=True, null=True)
    id_parag = models.IntegerField(blank=True, null=True)
    idtowr = models.TextField(blank=True, null=True)
    datsp = models.TextField(blank=True, null=True)
    ilosp = models.FloatField(blank=True, null=True)
    cenad = models.FloatField(blank=True, null=True)
    cenaz = models.FloatField(blank=True, null=True)
    vatsp = models.IntegerField(blank=True, null=True)
    cendn = models.FloatField(blank=True, null=True)
    gdzsp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sprzedaz_08'


class Sprzedaz3Mce(models.Model):
    bloz = models.TextField()
    apteka = models.IntegerField()
    sprzedaz = models.FloatField()
    pierwsza_data = models.TextField()
    id_ostatnia_sprzedaz = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sprzedaz_3_mce'
        unique_together = (('bloz', 'apteka'),)


class SprzedazPrzelewy(models.Model):
    dataw = models.TextField(db_collation='utf8_polish_ci')
    nrfv = models.TextField(db_collation='utf8_polish_ci')
    kwota = models.FloatField()
    datap = models.TextField(db_collation='utf8_polish_ci')
    apteka = models.IntegerField()
    zaplacone = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sprzedaz_przelewy'


class TestRem(models.Model):
    apteka = models.TextField(db_collation='utf8_polish_ci')
    data = models.TextField(db_collation='utf8_polish_ci')
    wynik_1 = models.TextField(db_collation='utf8_polish_ci')
    wynik_2 = models.IntegerField()
    len_apteka = models.IntegerField()
    len_baza = models.IntegerField()
    sprz_apt = models.IntegerField()
    sprz_zpt = models.IntegerField()
    zak_apt = models.IntegerField()
    zak_zpt = models.IntegerField()
    ind_apt = models.IntegerField()
    ind_zpt = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'test_rem'


class Urlopy(models.Model):
    id_urlopy = models.AutoField(primary_key=True)
    pracownik = models.TextField()
    rodzaj = models.TextField()
    data = models.TextField()
    urlop_rok = models.TextField()
    uwagi = models.TextField()

    class Meta:
        managed = False
        db_table = 'urlopy'


class Uzytkownicy(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.TextField()
    pass_field = models.TextField(db_column='pass')  # Field renamed because it was a Python reserved word.
    uprawnienia = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'uzytkownicy'


class Zakupy02(models.Model):
    id_zak = models.IntegerField(primary_key=True)
    wartosc = models.FloatField(blank=True, null=True)
    dat_zak_fv = models.TextField(blank=True, null=True)
    datap = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zakupy_02'


class Zakupy03(models.Model):
    id_zak = models.IntegerField(primary_key=True)
    wartosc = models.FloatField(blank=True, null=True)
    dat_zak_fv = models.TextField(blank=True, null=True)
    datap = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zakupy_03'


class Zakupy04(models.Model):
    id_zak = models.IntegerField(primary_key=True)
    wartosc = models.FloatField(blank=True, null=True)
    dat_zak_fv = models.TextField(blank=True, null=True)
    datap = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zakupy_04'


class Zakupy05(models.Model):
    id_zak = models.IntegerField(primary_key=True)
    wartosc = models.FloatField(blank=True, null=True)
    dat_zak_fv = models.TextField(blank=True, null=True)
    datap = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zakupy_05'


class Zakupy06(models.Model):
    id_zak = models.IntegerField(primary_key=True)
    wartosc = models.FloatField(blank=True, null=True)
    dat_zak_fv = models.TextField(blank=True, null=True)
    datap = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zakupy_06'


class Zakupy07(models.Model):
    id_zak = models.IntegerField(primary_key=True)
    wartosc = models.FloatField(blank=True, null=True)
    dat_zak_fv = models.TextField(blank=True, null=True)
    datap = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zakupy_07'


class Zakupy08(models.Model):
    id_zak = models.IntegerField(primary_key=True)
    wartosc = models.FloatField(blank=True, null=True)
    dat_zak_fv = models.TextField(blank=True, null=True)
    datap = models.TextField(blank=True, null=True)
    nrfv = models.TextField(blank=True, null=True)
    dostawca = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zakupy_08'


class ZakupyHurtownie(models.Model):
    apteka = models.IntegerField()
    miesiac = models.TextField()
    data_akt = models.TextField()
    kwoty = models.TextField()
    procenty = models.TextField()

    class Meta:
        managed = False
        db_table = 'zakupy_hurtownie'


class Zamknij(models.Model):
    apteka = models.IntegerField()
    zamknij = models.IntegerField()
    pracuje = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zamknij'


class Zamowienia02(models.Model):
    id_zam = models.IntegerField(unique=True)
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'zamowienia_02'


class Zamowienia03(models.Model):
    id_zam = models.IntegerField(unique=True)
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'zamowienia_03'


class Zamowienia04(models.Model):
    id_zam = models.IntegerField(unique=True)
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'zamowienia_04'


class Zamowienia05(models.Model):
    id_zam = models.IntegerField(unique=True)
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'zamowienia_05'


class Zamowienia06(models.Model):
    id_zam = models.IntegerField(unique=True)
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'zamowienia_06'


class Zamowienia07(models.Model):
    id_zam = models.IntegerField(unique=True)
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'zamowienia_07'


class Zamowienia08(models.Model):
    id_zam = models.IntegerField(unique=True)
    nazwa = models.TextField()
    ilzam = models.TextField()
    datzm = models.TextField()
    gdzzm = models.TextField()
    bloz = models.TextField()
    krotkie_daty = models.TextField()
    s02 = models.TextField()
    s03 = models.TextField()
    s04 = models.TextField()
    s05 = models.TextField()
    s06 = models.TextField()
    s07 = models.TextField()
    s08 = models.TextField()
    zalegajace = models.TextField()
    sp02 = models.TextField()
    sp03 = models.TextField()
    sp04 = models.TextField()
    sp05 = models.TextField()
    sp06 = models.TextField()
    sp07 = models.TextField()
    sp08 = models.TextField()

    class Meta:
        managed = False
        db_table = 'zamowienia_08'


class ZamowieniaGodziny(models.Model):
    apteka = models.IntegerField()
    data_klik = models.TextField()
    godz_klik = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zamowienia_godziny'
