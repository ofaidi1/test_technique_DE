import pandas as pd
import logging

LOGGER = logging.getLogger(__name__)


import pandas as pd
import re

def clean_invalid_characters(df):
    """
    Clean invalid characters (like \\xc3\\x28) from all string columns in a DataFrame.
    """
    # Regular expression to match invalid characters
    invalid_char_pattern = r"\\x[0-9a-fA-F]{2}"

    # Apply cleaning to all string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(
            lambda x: re.sub(invalid_char_pattern, "", x) if isinstance(x, str) else x
        )
    return df


def clean_data(data_df):
    """
    Clean data an unify date format

    """
    data_df = clean_invalid_characters(data_df)
    try:
        data_df['date'] = pd.to_datetime(data_df['date'], format='mixed').dt.date.astype(str)   
        data_df = data_df.mask(data_df == '')
        data_df = data_df.fillna("")
    except Exception as e:
        LOGGER.error("Error when cleaning data. Message: {}".format(e))

    return data_df
