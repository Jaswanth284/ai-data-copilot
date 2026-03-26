import pandas as pd
from openai import OpenAI

from app.core.config import settings


def build_dataset_context(df: pd.DataFrame) -> str:
    preview = df.head(5).to_dict(orient="records")
    columns = df.columns.tolist()
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    row_count = int(df.shape[0])
    column_count = int(df.shape[1])

    return (
        f"Dataset overview:\n"
        f"- Rows: {row_count}\n"
        f"- Columns: {column_count}\n"
        f"- Column names: {columns}\n"
        f"- Data types: {dtypes}\n"
        f"- Preview rows: {preview}\n"
    )


def ask_llm_about_dataset(df: pd.DataFrame, question: str) -> str:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is missing in .env")

    client = OpenAI(api_key=settings.openai_api_key)

    dataset_context = build_dataset_context(df)

    prompt = f"""
You are a helpful data assistant.

Use the dataset context below to answer the user's question.
Be concise, accurate, and only use the provided dataset context.

{dataset_context}

User question:
{question}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text