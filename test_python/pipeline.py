import json
import pandas as pd
import logging
from src.ingest import load_csv, load_json_as_dataframe
from src.clean import clean_data
from src.transform import find_mentions, build_drug_mentions, build_journal_mentions
from src.analysis import journal_with_most_unique_drugs, related_drugs_via_pubmed
from src.output import save_to_json
from config import DRUGS_PATH, CLINICAL_TRIALS_PATH, PUBMED_CSV_PATH, PUBMED_JSON_PATH, OUTPUT_PATH, TARGET_DRUG


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
LOGGER = logging.getLogger(__name__)

def run_pipeline():
    LOGGER.info("Pipeline execution started.")

    try:
        # Load data
        LOGGER.info("Loading input data...")
        drugs_df = load_csv(DRUGS_PATH)
        clinical_trials_df = load_csv(CLINICAL_TRIALS_PATH)
        pubmed_csv_df = load_csv(PUBMED_CSV_PATH)
        pubmed_json_df = load_json_as_dataframe(PUBMED_JSON_PATH)
        pubmed_combined_df = pd.concat([pubmed_csv_df, pubmed_json_df], ignore_index=True)

        # Clean data
        LOGGER.info("Cleaning data...")
        pubmed_combined_df = pubmed_combined_df.drop_duplicates()
        clinical_trials_df = clean_data(clinical_trials_df)
        pubmed_combined_df = clean_data(pubmed_combined_df)

        # Transform data
        LOGGER.info("Transforming data...")
        clinical_mentions = find_mentions(drugs_df, clinical_trials_df, "scientific_title", "clinical_trial")
        pubmed_mentions = find_mentions(drugs_df, pubmed_combined_df, "title", "pubmed")
        all_mentions = clinical_mentions + pubmed_mentions

        # Build the output JSON structure
        LOGGER.info("Building output JSON...")
        drugs_section = build_drug_mentions(drugs_df, all_mentions)
        journals_section = build_journal_mentions(all_mentions)
        final_structure = {
            "drugs": drugs_section,
            "journals": journals_section
        }

        # Save output
        save_to_json(final_structure, OUTPUT_PATH)
        LOGGER.info(f"Output successfully saved to {OUTPUT_PATH}.")

        # Ad-hoc Processing
                # Ad-hoc Processing
        LOGGER.info("=" * 50)
        LOGGER.info("Performing ad-hoc analyses.")
        LOGGER.info("=" * 50)
        top_journal = journal_with_most_unique_drugs(final_structure)
        LOGGER.info(f"Journal with most unique drugs: {top_journal}")

        related_drugs = related_drugs_via_pubmed(final_structure, TARGET_DRUG)
        LOGGER.info(f"Drugs related to {TARGET_DRUG} via PubMed: {related_drugs}")

    except Exception as e:
        LOGGER.error(f"Pipeline failed with error: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()
