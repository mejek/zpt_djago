from django.db import connection

def set_cursor(cursor):
    cursor.execute("SET NAMES utf8mb4;")  # or utf8 or any other charset you want to handle
    cursor.execute("SET CHARACTER SET utf8mb4;")  # same as above
    cursor.execute("SET character_set_connection=utf8mb4;")

def zpt_query_fetchone(query):
    with connection.cursor() as cursor:
        set_cursor(cursor)
        cursor.execute(query)
        wynik = cursor.fetchone()
        cursor.close()
        connection.close()

    return wynik

def zpt_query_fetchall(query):
    with connection.cursor() as cursor:
        set_cursor(cursor)
        cursor.execute(query)
        wynik = cursor.fetchall()
        cursor.close()
        connection.close()

    return wynik

def zpt_query_modify(query):
    with connection.cursor() as cursor:
        set_cursor(cursor)
        cursor.execute(query)
        cursor.close()
        connection.close()
