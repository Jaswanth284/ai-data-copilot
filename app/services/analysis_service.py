import pandas as pd


def normalize_question(question: str):
    return question.lower().strip()


def detect_intent(question: str):
    if any(word in question for word in ["row", "rows", "records", "entries", "count"]):
        return "row_count"

    if any(word in question for word in ["total revenue", "sum", "total"]):
        return "total_revenue"

    if any(word in question for word in ["average", "mean"]):
        return "average_revenue"

    if any(word in question for word in ["max", "highest", "top"]):
        return "max_revenue"

    return "unknown"


def answer_question(df: pd.DataFrame, question: str):
    question = normalize_question(question)
    intent = detect_intent(question)

    if intent == "row_count":
        return {"answer": int(df.shape[0])}

    if intent == "total_revenue":
        if "revenue" in df.columns:
            return {"answer": float(df["revenue"].sum())}

    if intent == "average_revenue":
        if "revenue" in df.columns:
            return {"answer": float(df["revenue"].mean())}

    if intent == "max_revenue":
        if "revenue" in df.columns:
            row = df.loc[df["revenue"].idxmax()]
            return {"answer": row.to_dict()}

    return {"answer": "Sorry, I couldn't understand the question."}