import pandas as pd
from pathlib import Path


def load_dataset(file_path: Path):
    return pd.read_csv(file_path)


def get_dataset_summary(df):
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "preview": df.head(5).to_dict(orient="records"),
    }