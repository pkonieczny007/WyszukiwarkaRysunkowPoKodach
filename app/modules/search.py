import os

def find_file(drawing_number, order_number, dokumentacja_path, realizowane_path):
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
                                return os.path.join(sub_root, file)

    # Search entire dokumentacja_path if not found or no order_number
    for root, _, files in os.walk(dokumentacja_path):
        for file in files:
            if file.startswith(drawing_number) and file.endswith('.pdf'):
                return os.path.join(root, file)

    # Search realizowane_path if still not found
    for root, _, files in os.walk(realizowane_path):
        for file in files:
            if file.startswith(drawing_number) and file.endswith('.pdf'):
                return os.path.join(root, file)

    # If still not found, try searching for files containing the drawing number
    for root, _, files in os.walk(dokumentacja_path):
        for file in files:
            if drawing_number in file and file.endswith('.pdf'):
                return os.path.join(root, file)

    for root, _, files in os.walk(realizowane_path):
        for file in files:
            if drawing_number in file and file.endswith('.pdf'):
                return os.path.join(root, file)

    return None
