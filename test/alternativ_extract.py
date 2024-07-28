from pdfminer.high_level import extract_text
import os

def extract_text_from_pdf(pdf_path):
    """Extrahiert den Text aus einer PDF-Datei."""
    return extract_text(pdf_path)

def save_text_to_file(text, output_path):
    """Speichert den extrahierten Text in einer Textdatei."""
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == "__main__":
    # Pfade zu den PDF-Dateien
    pdf_paths = [
        r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\ACT100.23.EN-US.pdf",
        r"C:\Users\602648\OneDrive - BildungsCentrum der Wirtschaft gemeinnützige Gesellschaft mbH\Bachelor\books - for code\ACT200.23.EN-US.pdf"
    ]

    # Verarbeite jede PDF-Datei
    for pdf_path in pdf_paths:
        # Erstelle den Namen für die Ausgabedatei
        output_file = os.path.splitext(os.path.basename(pdf_path))[0] + "_auszug.txt"
        extracted_text = extract_text_from_pdf(pdf_path)
        save_text_to_file(extracted_text, output_file)
        print(f"Text wurde erfolgreich extrahiert und in '{output_file}' gespeichert.")
