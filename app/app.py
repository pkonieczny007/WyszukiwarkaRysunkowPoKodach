import os
import pandas as pd
from flask import Flask, request, render_template, send_file

# Flask app logic
app = Flask(__name__)

# Load CSV data
data_path = "app/data/export.csv"
dokumentacja_path = "\\\\QNAP-ENERGO\\tmp\\dokumentacja_TEST_SKANERA"
try:
    data = pd.read_csv(data_path, sep=';')
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
        
        # Search for PrdRef
        result = data[data['RecID'] == rec_id]
        if not result.empty:
            prd_ref = result.iloc[0]['PrdRef']
            try:
                # Extract drawing number and order number
                parts = prd_ref.split('_')
                drawing_number = parts[2]  # rysunek
                order_number = parts[6]    # zlecenie

                # Search folder by order number
                folder_path = os.path.join(dokumentacja_path, order_number)
                if not os.path.exists(folder_path):
                    folder_path = dokumentacja_path  # Search entire folder if order folder doesn't exist

                # Find the drawing file
                found_file = None
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        if file.startswith(drawing_number) and file.endswith('.pdf'):
                            found_file = os.path.join(root, file)
                            break
                    if found_file:
                        break

                if found_file:
                    return send_file(found_file, mimetype='application/pdf')
                else:
                    return f"Nie znaleziono rysunku dla numeru: {drawing_number} w formacie .pdf"
            except IndexError:
                return f"Nie udało się wyodrębnić informacji z PrdRef: {prd_ref}"
        else:
            return "Nie znaleziono PrdRef dla podanego kodu."
    except ValueError:
        return "Nieprawidłowy format kodu."

if __name__ == '__main__':
    app.run(debug=True)
