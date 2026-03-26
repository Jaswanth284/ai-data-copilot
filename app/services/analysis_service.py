import pandas as pd


def answer_question(df: pd.DataFrame, question: str):
    question = question.lower()

    if "total revenue" in question:
        if "revenue" in df.columns:
            return {"answer": float(df["revenue"].sum())}

    if "average revenue" in question:
        if "revenue" in df.columns:
            return {"answer": float(df["revenue"].mean())}

    if "highest revenue" in question:
        if "revenue" in df.columns:
            row = df.loc[df["revenue"].idxmax()]
            return {"answer": row.to_dict()}

    if "how many rows" in question:
        return {"answer": int(df.shape[0])}

    return {"answer": "Sorry, I don't understand the question yet."}