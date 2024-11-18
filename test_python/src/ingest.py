import pandas as pd
import json

def load_csv(filepath):
    """Load a CSV file as a pandas DataFrame."""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        raise ValueError(f"Error loading CSV file: {filepath}. Details: {e}")


def fix_json_errors(raw_content):
    
    """ Eliminate commas before closing brackets or braces """
    fixed_content = raw_content.replace(",\n]", "\n]").replace(",\n}", "\n}")
    return fixed_content



def load_json_as_dataframe(filepath):
    """
    Load a JSON file and convert it to a pandas DataFrame.
    Fixes common JSON issues during the loading process.

    """
    try:
        with open(filepath, 'r') as file:
            raw_content = file.read()

        # Fix JSON errors
        fixed_content = fix_json_errors(raw_content)

        # Load the corrected JSON content
        data = json.loads(fixed_content)
        return pd.DataFrame(data)
    
    except Exception as e:
        raise ValueError(f"Unexpected error when loading JSON file: {filepath}. Details: {e}")