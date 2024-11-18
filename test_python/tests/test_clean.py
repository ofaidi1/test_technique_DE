import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.clean import clean_data

def test_clean_data():
    # Test cleaning a DataFrame with unwanted characters and date normalization
    data = {
        "title": ["  Example Title 1  ", "Example Title 2 \\xc3\\x28 "],
        "journal": ["Journal A \\xc3\\x28", "  Journal B  "],
        "date": ["2023-01-01", "2023/01/05"],
    }
    df = pd.DataFrame(data)

    # Apply cleaning function
    cleaned_df = clean_data(df)


    # Verify special characters are removed
    assert "\\xc3\\x28" not in cleaned_df.iloc[0]["journal"], "Special characters should be removed from 'journal'."
    assert "\\xc3\\x28" not in cleaned_df.iloc[1]["title"], "Special characters should be removed from 'title'."
    # Verify date format normalization
    assert cleaned_df.iloc[0]["date"] == "2023-01-01", "Date format should be standardized to YYYY-MM-DD."
    assert cleaned_df.iloc[1]["date"] == "2023-01-05", "Date format should handle variations."