from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import RAW_DATA_DIR
from app.services.llm_service import ask_llm_about_dataset

router = APIRouter()


class AIAskRequest(BaseModel):
    filename: str
    question: str


@router.post("/ask")
def ask_ai(request: AIAskRequest):
    file_path = Path(RAW_DATA_DIR) / request.filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        df = pd.read_csv(file_path)
        answer = ask_llm_about_dataset(df, request.question)

        return {
            "question": request.question,
            "answer": answer,
            "source": "AI + dataset"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))