def find_drawing(rec_id, data):
    """
    Wyszukuje rysunek na podstawie RecID.
    """
    result = data[data['RecID'] == rec_id]
    if not result.empty:
        prd_ref = result.iloc[0]['PrdRef']
        drawing_number = prd_ref.split('_')[2]  # Ekstrahowanie numeru rysunku
        return {
            "drawing": drawing_number,
            "date": result.iloc[0]['CrtDate']
        }
    else:
        return None
