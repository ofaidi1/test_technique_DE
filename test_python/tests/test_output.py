import os
import sys
import json
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.output import save_to_json

def test_save_to_json():
    """
    Test saving data to a JSON file and verifying the file content.
    """
    # Sample data to save
    sample_data = {
        "drugs": [
            {"name": "DrugA", "mentions": [{"type": "pubmed", "id": 1, "journal": "Journal A"}]},
            {"name": "DrugB", "mentions": []}
        ],
        "journals": [
            {"name": "Journal A", "mentions": [{"drug": "DrugA", "source": "pubmed", "id": 1}]}
        ]
    }

    # Path to temporary test file
    test_file_path = "tests/test_data/output_test.json"

    # Ensure the test directory exists
    os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

    try:
        # Save data to JSON file
        save_to_json(sample_data, test_file_path)

        # Verify the file was created
        assert os.path.exists(test_file_path), "JSON file was not created."

        # Load the file content and verify
        with open(test_file_path, "r") as file:
            loaded_data = json.load(file)

        assert loaded_data == sample_data, "The saved JSON content does not match the input data."

    finally:
        # Cleanup: Remove the test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
