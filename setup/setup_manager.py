import os

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

    print(f"Project structure created at {base_path}")

# Example usage
base_directory = "./my_project"
create_project_structure(base_directory)
