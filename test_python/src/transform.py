def extract_drugs_from_title(title, drugs):
    """
    Extract drugs from the title of the publication.
    """
    mentions = []
    for drug_name in drugs:
        if drug_name.lower() in (title or "").lower():
            mentions.append(drug_name)
    return mentions




def find_mentions(drugs_df, source_df, title_col, source_name):
    """
    Find drug mentions in publication titles.

    """
    # List of all drug names
    drug_names = drugs_df["drug"].tolist()

    # Initialize mentions
    mentions = []

    # Iterate through the source DataFrame
    for _, article in source_df.iterrows():
        matched_drugs = extract_drugs_from_title(article[title_col], drug_names)

        for drug_name in matched_drugs:
            drug_info = drugs_df[drugs_df["drug"] == drug_name].iloc[0]
            mentions.append({
                "drug": drug_name,
                "drug_id": drug_info["atccode"],
                "source": source_name,
                "id": article["id"],
                "title": article[title_col],
                "journal": article["journal"],
                "date": article["date"]
            })

    return mentions



def build_drug_mentions(drugs_df, mentions):
    """
    Build the 'drugs' section of the output JSON.
    """
    drugs_output = []

    for _, drug in drugs_df.iterrows():
        drug_name = drug["drug"]
        drug_id = drug["atccode"]

        # Filter mentions related to this drug
        drug_mentions = []
        for mention in mentions:
            if mention["drug"] == drug_name:
                drug_mentions.append({
                    "type": mention["source"],
                    "id": mention["id"],
                    "title": mention["title"],
                    "journal": mention["journal"],
                    "date": mention["date"]
                })

        # Append the drug's information and its mentions
        drugs_output.append({
            "name": drug_name,
            "drug_id": drug_id,
            "mentions": drug_mentions
        })

    return drugs_output




def build_journal_mentions(mentions):
    """
    Build the 'journals' section of the JSON structure with drug details.

    """
    # Initialize a dictionary to group mentions by journal
    journals = {}

    for mention in mentions:
        journal_name = mention["journal"]

        if journal_name not in journals:
            journals[journal_name] = []

        # Append the mention details to the journal
        journals[journal_name].append({
            "drug": mention["drug"],
            "drug_id": mention.get("drug_id"),
            "source": mention["source"],
            "id": mention["id"],
            "date": mention["date"]
        })

    # Build the output structure
    journal_output = []
    for journal, mentions_list in journals.items():
        journal_output.append({
            "name": journal,
            "mentions": mentions_list
        })

    return journal_output
