import os
import subprocess
import sys

def install_requirements():
    requirements_path = "requirements.txt"
    
    if not os.path.exists(requirements_path):
        print(f"Plik {requirements_path} nie istnieje. Upewnij się, że znajduje się w tym samym katalogu.")
        return

    try:
        print(f"Instalacja modułów z {requirements_path}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("Wszystkie moduły zostały zainstalowane pomyślnie.")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas instalacji: {e}")
    except Exception as ex:
        print(f"Wystąpił nieoczekiwany błąd: {ex}")

if __name__ == "__main__":
    install_requirements()
