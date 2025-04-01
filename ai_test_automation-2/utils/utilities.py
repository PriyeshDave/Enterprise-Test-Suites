import pandas as pd

def extract_schema(df):
    schema = {col: str(df[col].dtype) for col in df.columns}
    return schema