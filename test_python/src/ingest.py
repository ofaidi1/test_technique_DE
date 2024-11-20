import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
LOGGER = logging.getLogger(__name__)

def load_csv(filepath):
    """Load a CSV file as a pandas DataFrame."""
    try:
        LOGGER.info(f"Loading CSV file: {filepath}")
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        LOGGER.error(f"Error loading CSV file: {filepath}. Details: {e}")
        raise ValueError(f"Error loading CSV file: {filepath}. Details: {e}")

def fix_json_errors(raw_content):
    """Eliminate commas before closing brackets or braces."""
    fixed_content = raw_content.replace(",\n]", "\n]").replace(",\n}", "\n}")
    return fixed_content

def load_json_as_dataframe(filepath):
    """
    Load a JSON file and convert it to a pandas DataFrame.
    Fixes common JSON issues during the loading process.
    """
    try:
        LOGGER.info(f"Loading JSON file: {filepath}")
        with open(filepath, 'r') as file:
            raw_content = file.read()

        # Fix JSON errors
        fixed_content = fix_json_errors(raw_content)

        # Load the corrected JSON content
        data = json.loads(fixed_content)
        return pd.DataFrame(data)
    except Exception as e:
        LOGGER.error(f"Unexpected error when loading JSON file: {filepath}. Details: {e}")
        raise ValueError(f"Unexpected error when loading JSON file: {filepath}. Details: {e}")
