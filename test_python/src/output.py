import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
LOGGER = logging.getLogger(__name__)

def save_to_json(data, filepath):
    """ 
    Save a Python object as a JSON file with decoded Unicode characters.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        LOGGER.error(f"Error saving JSON to {filepath}. Details: {e}")
        raise ValueError(f"Error saving JSON to {filepath}. Details: {e}")
