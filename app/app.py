import os
import pandas as pd
from flask import Flask, request, render_template

# Flask app logic
app = Flask(__name__)

# Load CSV data
data_path = "app/data/export.csv"
dokumentacja_path = "\\\\QNAP-ENERGO\\Dokumentacja_rysunki\\001. GIĘCIE"
realizowane_folder = "\\\\QNAP-ENERGO\\Dokumentacja_rysunki\\00 ZREALIZOWANO"
try:
    data = pd.read_csv(data_path, sep=';')
    print("Dane załadowane poprawnie z:", data_path)
except Exception as e:
    print(f"Error loading data from {data_path}: {e}")
    data = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    barcode = request.form['barcode']
    try:
        # Extract RecID from barcode
        rec_id = int(barcode.split('#')[-1]) if '#' in barcode else int(barcode)
        print(f"RecID odczytany: {rec_id}")

        # Search for PrdRef
        result = data[data['RecID'] == rec_id]
        if not result.empty:
            prd_ref = result.iloc[0]['PrdRef']
            print(f"PrdRef znaleziony: {prd_ref}")
            try:
                # Extract drawing number and order number
                parts = prd_ref.split('_')
                drawing_number = parts[2]  # rysunek
                order_number = parts[6]    # zlecenie
                print(f"Numer rysunku: {drawing_number}, Numer zlecenia: {order_number}")

                # Search folder by order number
                folder_path = os.path.join(dokumentacja_path, order_number)
                found_files = []

                # Search specific order folder
                if os.path.exists(folder_path):
                    for root, _, files in os.walk(folder_path):
                        for file in files:
                            if file.startswith(drawing_number) and file.endswith('.pdf'):
                                found_files.append(os.path.join(root, file))

                # Search "00 ZREALIZOWANO" folder if no results
                if not found_files:
                    for root, _, files in os.walk(realizowane_folder):
                        for file in files:
                            if file.startswith(drawing_number) and file.endswith('.pdf'):
                                found_files.append(os.path.join(root, file))

                # Render results
                if found_files:
                    return render_template('results.html', main_file=found_files[0], additional_files=found_files[1:])
                else:
                    return render_template('error.html', message=f"Nie znaleziono rysunków dla numeru: {drawing_number}")

            except IndexError:
                return render_template('error.html', message=f"Nie udało się wyodrębnić informacji z PrdRef: {prd_ref}")
        else:
            return render_template('error.html', message="Nie znaleziono PrdRef dla podanego kodu.")
    except ValueError:
        return render_template('error.html', message="Nieprawidłowy format kodu.")

if __name__ == '__main__':
    app.run(debug=True)
