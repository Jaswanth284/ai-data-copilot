from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

from app.core.config import RAW_DATA_DIR
from app.services.profiling_service import generate_dataset_profile

router = APIRouter()


@router.get("/profile")
def profile_dataset(filename: str):
    file_path = Path(RAW_DATA_DIR) / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        df = pd.read_csv(file_path)
        profile = generate_dataset_profile(df)

        return {
            "filename": filename,
            "profile": profile
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))