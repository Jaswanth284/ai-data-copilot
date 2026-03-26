from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.core.config import RAW_DATA_DIR
from app.services.dataset_service import load_dataset, get_dataset_summary

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Check if file is provided
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Allow only CSV files
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    # Save file to raw data folder
    file_path = Path(RAW_DATA_DIR) / file.filename

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Load dataset
        df = load_dataset(file_path)

        # Get summary
        summary = get_dataset_summary(df)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))