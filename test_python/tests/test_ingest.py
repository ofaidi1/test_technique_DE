import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.ingest import load_csv, load_json_as_dataframe

def test_load_csv():
    # Test loading a valid CSV file
    test_csv = "tests/test_data/test_file.csv"
    df = load_csv(test_csv)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_json_as_dataframe():
    # Path to a valid JSON file
    test_json = "tests/test_data/test_file.json"

    # Load JSON and verify output
    df = load_json_as_dataframe(test_json)
    assert isinstance(df, pd.DataFrame), "The output should be a pandas DataFrame."
    assert not df.empty, "The DataFrame should not be empty for a valid JSON."
