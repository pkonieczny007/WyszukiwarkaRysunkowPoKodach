import os
import pandas as pd
from flask import Flask, request, send_file
from modules.search import find_file  # Import funkcji wyszukiwania

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

                # Use the external search function
                found_file = find_file(drawing_number, order_number, dokumentacja_path, realizowane_path)

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
