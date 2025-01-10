def parse_barcode(barcode):
    """
    Parsuje kod kreskowy i zwraca RecID.
    """
    try:
        return int(barcode.split('#')[-1])
    except ValueError:
        raise ValueError("Nieprawidłowy format kodu kreskowego.")
