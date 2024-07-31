import psycopg2
import configparser
import os

def read_db_config(filename='config.ini', section='database'):
    parser = configparser.ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db

def connect():
    try:
        params = read_db_config(filename='.streamlit/config.ini')  # Pfad zur config.ini-Datei anpassen
        conn = psycopg2.connect(**params)
        return conn
    except Exception as error:
        print(f"Fehler bei der Verbindung zur Datenbank: {error}")
        return None

def create_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL
                )
            """)
            conn.commit()
    except Exception as error:
        print(f"Fehler beim Erstellen der Tabelle: {error}")

def insert_book(conn, title, author, content):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO books (title, author, content)
                VALUES (%s, %s, %s)
            """, (title, author, content))
            conn.commit()
    except Exception as error:
        print(f"Fehler beim Einfügen des Buches: {error}")

def get_book_content_from_db(conn, book_title):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT content FROM books WHERE title = %s
            """, (book_title,))
            result = cursor.fetchone()
            return result[0] if result else "Buchinhalt nicht gefunden"
    except Exception as error:
        print(f"Fehler beim Abrufen des Buchinhalts: {error}")
        return "Fehler beim Abrufen des Buchinhalts"

def get_all_books(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT title FROM books
            """)
            result = cursor.fetchall()
            return [row[0] for row in result]
    except Exception as error:
        print(f"Fehler beim Abrufen der Bücher: {error}")
        return []
