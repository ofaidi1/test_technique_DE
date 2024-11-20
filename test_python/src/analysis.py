
def journal_with_most_unique_drugs(pipeline_output):
    """ 
    Find the journal that mentions the most unique drugs.
    """
    max_drugs = 0
    top_journal = None

    for journal in pipeline_output["journals"]:
        unique_drugs = {mention["drug"] for mention in journal["mentions"]}
        if len(unique_drugs) > max_drugs:
            max_drugs = len(unique_drugs)
            top_journal = journal["name"]

    return top_journal


def related_drugs_via_pubmed(pipeline_output, target_drug):
    """
    Find all drugs mentioned in the same journals as the target drug, considering only PubMed sources. 
    """
    target_journals = set()
    related_drugs = set()

    # Identify journals linked to the target drug via PubMed
    for drug in pipeline_output["drugs"]:
        if drug["name"] == target_drug:
            target_journals = {
                mention["journal"]
                for mention in drug["mentions"]
                if mention["type"] == "pubmed"
            }
            break

    # Find other drugs mentioned in the same journals
    for journal in pipeline_output["journals"]:
        if journal["name"] in target_journals:
            related_drugs.update(
                mention["drug"]
                for mention in journal["mentions"]
                if mention["source"] == "pubmed" and mention["drug"] != target_drug
            )

    # Return a message if no related drugs are found
    if not related_drugs:
        return f"No drugs found related to {target_drug} via PubMed."

    return related_drugs
