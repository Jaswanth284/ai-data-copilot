from pathlib import Path
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import RAW_DATA_DIR
from app.services.rag_service import build_rag_index_from_dataframe, ask_rag

router = APIRouter()


class RAGIndexRequest(BaseModel):
    filename: str


class RAGAskRequest(BaseModel):
    question: str
    top_k: int = 3


@router.post("/index")
def create_rag_index(request: RAGIndexRequest):
    file_path = Path(RAW_DATA_DIR) / request.filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        df = pd.read_csv(file_path)
        result = build_rag_index_from_dataframe(df)
        return {
            "filename": request.filename,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask")
def ask_question_with_rag(request: RAGAskRequest):
    try:
        result = ask_rag(request.question, top_k=request.top_k)
        return {
            "question": request.question,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))