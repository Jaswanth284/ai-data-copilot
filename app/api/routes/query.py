from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

from app.core.config import RAW_DATA_DIR
from app.services.analysis_service import answer_question

router = APIRouter()


@router.get("/ask")
def ask_question(question: str, filename: str):
    file_path = Path(RAW_DATA_DIR) / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        df = pd.read_csv(file_path)
        response = answer_question(df, question)

        return {
            "question": question,
            "filename": filename,
            "response": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))