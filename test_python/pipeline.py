import json
import pandas as pd
from src.ingest import load_csv, load_json_as_dataframe
from src.clean import clean_data
from src.transform import find_mentions, build_drug_mentions, build_journal_mentions
from src.analysis import journal_with_most_unique_drugs, related_drugs_via_pubmed
from src.output import save_to_json

def run_pipeline():

    # Load  configuration file
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Paths to input data
    drugs_path = "data/drugs.csv"
    clinical_trials_path = "data/clinical_trials.csv"
    pubmed_csv_path = "data/pubmed.csv"
    pubmed_json_path = "data/pubmed.json"
    output_path = "output/drugs_mentions.json"

    # Load data
    drugs_df = load_csv(drugs_path)
    clinical_trials_df = load_csv(clinical_trials_path)
    pubmed_csv_df = load_csv(pubmed_csv_path)
    pubmed_json_df = load_json_as_dataframe(pubmed_json_path)
    pubmed_combined_df = pd.concat([pubmed_csv_df, pubmed_json_df], ignore_index=True)

    # Clean data
    pubmed_combined_df = pubmed_combined_df.drop_duplicates()
    clinical_trials_df = clean_data(clinical_trials_df)
    pubmed_combined_df = clean_data(pubmed_combined_df)


    # Transform data
    clinical_mentions = find_mentions(drugs_df, clinical_trials_df, "scientific_title", "clinical_trial")
    pubmed_mentions = find_mentions(drugs_df, pubmed_combined_df, "title", "pubmed")
    all_mentions = clinical_mentions + pubmed_mentions 

    # Build the output JSON structure
    drugs_section = build_drug_mentions(drugs_df, all_mentions)
    journals_section = build_journal_mentions(all_mentions)

    final_structure = {
        "drugs": drugs_section,
        "journals": journals_section
    }

    # Save output
    save_to_json(final_structure, output_path)

    # Load the generated JSON output
    with open(output_path, "r") as file:
        pipeline_output = json.load(file)

    # Ad-hoc Processing (Bonus) 1 : Identify the journal that mentions the most unique drugs
    top_journal = journal_with_most_unique_drugs(pipeline_output)
    print(f"The journal that mentions the most unique drugs: {top_journal}")

    # Ad-hoc Processing (Bonus) 2 : Find drugs related via PubMed for a specific drug
    target_drug = config.get("target_drug")
    related_drugs = related_drugs_via_pubmed(pipeline_output, target_drug)
    print(f"Drugs related to {target_drug} via PubMed: {related_drugs}")

if __name__ == "__main__":

    run_pipeline()
