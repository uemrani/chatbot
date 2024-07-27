#Indizierung des Texts
from elasticsearch import Elasticsearch
import os

def create_index(es_client, index_name):
    """Erstellt einen neuen Index in Elasticsearch."""
    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name)
        print(f"Index '{index_name}' wurde erstellt.")

def index_text(es_client, index_name, file_name, content):
    """Indexiert den extrahierten Text in Elasticsearch."""
    document = {
        'file_name': file_name,
        'content': content
    }
    es_client.index(index=index_name, document=document)

if __name__ == "__main__":
    # Elasticsearch-Client erstellen
    es_client = Elasticsearch()

    # Index-Name
    index_name = 'documents'
    
    # Erstelle den Index
    create_index(es_client, index_name)
    
    # Verzeichnispfad, in dem sich die extrahierten Texte befinden
    text_files_path = 'path_to_text_files'
    
    # Gehe durch alle Textdateien und indexiere den Inhalt
    for text_file in os.listdir(text_files_path):
        if text_file.endswith('.txt'):
            file_path = os.path.join(text_files_path, text_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                index_text(es_client, index_name, text_file, content)
                print(f"Text aus '{text_file}' wurde erfolgreich in Elasticsearch indexiert.")
