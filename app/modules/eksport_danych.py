import pyodbc
import pandas as pd
from datetime import datetime
import os
import shutil  # Do obsługi kopiowania plików

# Konfiguracja
server = 'ES-SRV\LANTEKSQL2019'
database = 'Energosolver_DB_0_9'
table = 'MMNN_MMOO_00000100'
columns = ['PrdRef', 'RecID', 'CrtDate']
username = 'sa'
password = ''
output_folder = r'C:\WyszukiwarkaRysunkowPoKodach\app\data'
export_file = os.path.join(output_folder, "export.csv")
old_export_file = os.path.join(output_folder, "oldexport.csv")


def ensure_directory_exists(directory):
    """Tworzy katalog, jeśli nie istnieje."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def fetch_all_records():
    """Pobiera wszystkie rekordy z bazy danych."""
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};"
    query = f"SELECT {', '.join(columns)} FROM {table} ORDER BY CrtDate ASC;"
    with pyodbc.connect(connection_string) as conn:
        df = pd.read_sql(query, conn)
        print(f"Kolumny w danych: {df.columns}")
        print(f"Pierwsze 5 rekordów:\n{df.head()}")
        return df


def manage_existing_files():
    """Zarządza istniejącymi plikami: kopiuje `export1.csv` do `oldexport1.csv`."""
    if os.path.exists(export_file):
        # Usunięcie starego pliku `oldexport1.csv` (jeśli istnieje)
        if os.path.exists(old_export_file):
            os.remove(old_export_file)
            print(f"Usunięto istniejący plik: {old_export_file}")

        # Kopiowanie `export1.csv` do `oldexport1.csv`
        shutil.copy2(export_file, old_export_file)
        print(f"Skopiowano plik: {export_file} do {old_export_file}")


def save_to_csv(data):
    """Zapisuje nowe dane do pliku `export1.csv`."""
    data.to_csv(export_file, index=False, sep=';', encoding='utf-8')
    print(f"Zapisano nowy plik: {export_file}")


def main():
    ensure_directory_exists(output_folder)
    print("Rozpoczęto eksport danych.")
    
    # Zarządzanie istniejącymi plikami
    manage_existing_files()
    
    # Pobieranie nowych danych z bazy
    all_data = fetch_all_records()
    if all_data.empty:
        print("Brak danych w bazie do zapisania.")
    else:
        save_to_csv(all_data)


if __name__ == "__main__":
    main()
