from pathlib import Path
from typing import Union

import pandas as pd

file_path = Path(__file__).resolve().parents[2] / "data" / "database.csv"
df = pd.read_csv(file_path)


# NOTE: Could have used model representation for company
# but for the test keeping it simple.
def get_company_details(company_name: str) -> Union[dict, None]:
    """
    Given a company name, returns company details from database.csv.

    Args:
        company_name (str): Name of company
    Returns:
         dict: object with company details
         None: if not found
    """
    filtered_df = df[df["Company Name"].str.lower() == company_name.lower()]
    if filtered_df.empty:
        return None
    return filtered_df.iloc[0].to_dict()
