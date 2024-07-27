import psycopg2
import configparser
import os
from pdfminer.high_level import extract_text

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
                    title TEXT,
                    section TEXT,
                    page_number INTEGER,
                    content TEXT,
                    keywords TEXT
                );
            """)
            conn.commit()
    except Exception as error:
        print(f"Fehler beim Erstellen der Tabelle: {error}")

def insert_data(conn, title, section, page_number, content, keywords):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM books
                WHERE title = %s AND section = %s AND page_number = %s AND content = %s AND keywords = %s;
            """, (title, section, page_number, content, keywords))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("""
                    INSERT INTO books (title, section, page_number, content, keywords)
                    VALUES (%s, %s, %s, %s, %s);
                """, (title, section, page_number, content, keywords))
                conn.commit()
                print(f"Daten erfolgreich eingefügt: {title}")
            else:
                print(f"Eintrag bereits vorhanden: {title}")
    except Exception as error:
        print(f"Fehler beim Einfügen der Daten: {error}")

def process_file(file_path, conn):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            title = os.path.basename(file_path).replace('_auszug.txt', '')
            section = "Unbekannt"  # Das kann angepasst werden, wenn du Abschnitte definieren kannst
            page_number = 1  # Wenn du Seitenzahlen extrahieren kannst, ersetze dies durch die tatsächliche Zahl
            keywords = ""  # Falls du Schlüsselwörter hast, füge sie hier ein

            insert_data(conn, title, section, page_number, content, keywords)
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei {file_path}: {e}")

def extract_text_from_pdf(pdf_path):
    """Extrahiert den Text aus einer PDF-Datei."""
    return extract_text(pdf_path)

def save_text_to_file(text, output_path):
    """Speichert den extrahierten Text in einer Textdatei."""
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == "__main__":
    # Extrahiere Text aus PDFs
    pdf_paths = [
        r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\ACT100.23.EN-US.pdf",
        r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\ACT200.23.EN-US.pdf"
    ]

    for pdf_path in pdf_paths:
        output_file = os.path.splitext(os.path.basename(pdf_path))[0] + "_auszug.txt"
        extracted_text = extract_text_from_pdf(pdf_path)
        save_text_to_file(extracted_text, output_file)
        print(f"Text wurde erfolgreich extrahiert und in '{output_file}' gespeichert.")

    # Verbinde mit der Datenbank und verarbeite die extrahierten Textdateien
    conn = connect()
    if conn:
        create_table(conn)
        
        text_files = [
            "ACT100.23.EN-US_auszug.txt",
            "ACT200.23.EN-US_auszug.txt"
        ]

        for text_file in text_files:
            process_file(text_file, conn)
        
        conn.close()
