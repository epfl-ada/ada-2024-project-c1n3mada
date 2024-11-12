import pandas as pd
import ast

def parse_date(date_str):
    """ 
    Parse a date string into a pandas datetime object.
    """
    try:
        return pd.to_datetime(date_str)
    except:
        return pd.NaT
    
def parse_dict(field):
    """
    Convert dictionary to a tuple (key, value) pairs
    """
    try:
        return [x for x in ast.literal_eval(field).items()]
    except:
        return []