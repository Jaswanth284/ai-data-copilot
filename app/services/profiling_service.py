import pandas as pd


def generate_dataset_profile(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=["number"])

    profile = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": {col: int(df[col].isnull().sum()) for col in df.columns},
        "numeric_summary": numeric_df.describe().to_dict() if not numeric_df.empty else {},
        "insights": generate_insights(df)
    }

    return profile


def generate_insights(df: pd.DataFrame):
    insights = []

    insights.append(f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.")

    missing_cols = [col for col in df.columns if df[col].isnull().sum() > 0]
    if missing_cols:
        insights.append(f"Columns with missing values: {', '.join(missing_cols)}.")
    else:
        insights.append("There are no missing values in the dataset.")

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if numeric_cols:
        for col in numeric_cols:
            insights.append(
                f"{col} has min={df[col].min()}, max={df[col].max()}, mean={round(df[col].mean(), 2)}."
            )

    return insights