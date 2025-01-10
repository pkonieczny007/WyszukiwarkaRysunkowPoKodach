import os
import pandas as pd
from flask import Flask, request, render_template

def create_project_structure(base_path):
    structure = {
        "app": [
            "templates",
            "static",
            "data",
            "modules",
        ],
        "setup": [],
        "prompt": [],
        "tmp": [],
        "tests": []
    }

    for folder, subfolders in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for subfolder in subfolders:
            os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)

    # Create common files
    open(os.path.join(base_path, "README.md"), 'w').close()
    open(os.path.join(base_path, "app", "app.py"), 'w').close()
    open(os.path.join(base_path, "app", "config.py"), 'w').close()

    print(f"Struktura projektu utworzona w {base_path}")

# Flask app logic
app = Flask(__name__)

# Load CSV data
data_path = "app/data/export.csv"
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
                # Extract drawing number
                drawing_number = prd_ref.split('_')[2]
                return f"Nr rysunku: {drawing_number} (PrdRef: {prd_ref})"
            except IndexError:
                return f"Nie udało się wyodrębnić nr rysunku. PrdRef: {prd_ref}"
        else:
            return "Nie znaleziono PrdRef dla podanego kodu."
    except ValueError:
        return "Nieprawidłowy format kodu."

if __name__ == '__main__':
    app.run(debug=True)

# Example usage
base_directory = "./WyszukiwarkaRysunkowPoKodach"
create_project_structure(base_directory)
