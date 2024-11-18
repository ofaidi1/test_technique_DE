import json

def save_to_json(data, filepath):
    """ 
    Save a Python object as a JSON file with decoded Unicode characters.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"JSON saved successfully to {filepath}")
    except Exception as e:
        raise ValueError(f"Error saving JSON to {filepath}. Details: {e}")