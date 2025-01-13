import os
import pandas as pd
from flask import Flask, request, send_file

# Flask app logic
app = Flask(__name__)

# Load CSV data
data_path = "app/data/export.csv"
dokumentacja_path = "\\\\QNAP-ENERGO\\Dokumentacja_rysunki\\001. GIĘCIE"
realizowane_path = "\\\\QNAP-ENERGO\\Dokumentacja_rysunki\\001. GIĘCIE\\00 ZREALIZOWANO"
try:
    data = pd.read_csv(data_path, sep=';')
except Exception as e:
    print(f"Error loading data from {data_path}: {e}")
    data = pd.DataFrame()

@app.route('/')
def index():
    return "<h1>Wyszukiwarka rysunków</h1><form method='POST' action='/search'><input type='text' name='barcode' placeholder='Wprowadź RecID'><button type='submit'>Szukaj</button></form>"

@app.route('/search', methods=['POST'])
def search():
    barcode = request.form['barcode']
    try:
        # Extract RecID from barcode
        rec_id = int(barcode.split('#')[-1]) if '#' in barcode else int(barcode)
        
        # Search for PrdRef
        result = data[data['RecID'] == rec_id]
        if not result.empty:
            prd_ref = result.iloc[0]['PrdRef']
            try:
                # Extract drawing number and optionally order number
                parts = prd_ref.split('_')
                drawing_number = parts[2]  # rysunek
                order_number = parts[6] if len(parts) > 6 else None

                # Initialize found_file
                found_file = None

                # Search for folder containing order number
                if order_number:
                    for root, dirs, files in os.walk(dokumentacja_path):
                        for dir_name in dirs:
                            if order_number in dir_name:
                                order_folder = os.path.join(root, dir_name)
                                for sub_root, _, sub_files in os.walk(order_folder):
                                    for file in sub_files:
                                        if file.startswith(drawing_number) and file.endswith('.pdf'):
                                            found_file = os.path.join(sub_root, file)
                                            break
                                    if found_file:
                                        break
                        if found_file:
                            break

                # Search entire dokumentacja_path if not found or no order_number
                if not found_file:
                    for root, _, files in os.walk(dokumentacja_path):
                        for file in files:
                            if file.startswith(drawing_number) and file.endswith('.pdf'):
                                found_file = os.path.join(root, file)
                                break
                        if found_file:
                            break

                # Search realizowane_path if still not found
                if not found_file:
                    for root, _, files in os.walk(realizowane_path):
                        for file in files:
                            if file.startswith(drawing_number) and file.endswith('.pdf'):
                                found_file = os.path.join(root, file)
                                break
                        if found_file:
                            break

                # Return the file or error
                if found_file:
                    return send_file(found_file, mimetype='application/pdf')
                else:
                    return f"<h1>Nie znaleziono rysunku dla numeru: {drawing_number}</h1><a href='/'>Wróć</a>"

            except IndexError:
                return f"<h1>Nie udało się wyodrębnić informacji z PrdRef: {prd_ref}</h1><a href='/'>Wróć</a>"
        else:
            return "<h1>Nie znaleziono PrdRef dla podanego kodu.</h1><a href='/'>Wróć</a>"
    except ValueError:
        return "<h1>Nieprawidłowy format kodu.</h1><a href='/'>Wróć</a>"

if __name__ == '__main__':
    app.run(debug=True)