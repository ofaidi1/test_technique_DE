
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.transform import find_mentions, build_drug_mentions, build_journal_mentions

def test_find_mentions():
    drugs_df = pd.DataFrame({
        "drug": ["DrugA", "DrugB"],
        "atccode": ["A01", "B02"]
    })

    source_df = pd.DataFrame({
        "title": ["DrugA is effective", "No mention here"],
        "id": [1, 2],
        "journal": ["Journal A", "Journal B"],
        "date": ["2023-01-01", "2023-01-02"]
    })

    mentions = find_mentions(drugs_df, source_df, "title", "pubmed")
def test_build_drug_mentions():
    drugs_df = pd.DataFrame({"drug": ["DrugA", "DrugB"], "atccode": ["A01", "B02"]})
    mentions = [
        {"drug": "DrugA", "id": 1, "title": "Test Title", "source": "pubmed", "journal": "Journal A", "date": "2023-01-01"}
    ]
    drugs_section = build_drug_mentions(drugs_df, mentions)

    assert len(drugs_section) == 2
    assert drugs_section[0]["name"] == "DrugA"
    assert drugs_section[0]["mentions"]

def test_build_journal_mentions():
    mentions = [
        {"drug": "DrugA", "id": 1, "title": "Test Title", "source": "pubmed", "journal": "Journal A", "date": "2023-01-01"},
        {"drug": "DrugB", "id": 2, "title": "Another Title", "source": "clinical_trial", "journal": "Journal A", "date": "2023-01-02"}
    ]
    journals_section = build_journal_mentions(mentions)

    assert len(journals_section) == 1
    assert journals_section[0]["name"] == "Journal A"
    assert len(journals_section[0]["mentions"]) == 2
