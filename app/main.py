from fastapi import FastAPI
from app.core.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from app.api.routes.upload import router as upload_router
from app.api.routes.query import router as query_router
from app.api.routes.profile import router as profile_router
from app.api.routes.ai import router as ai_router

app = FastAPI(title="AI Data Copilot")

app.include_router(upload_router, prefix="/datasets")
app.include_router(query_router, prefix="/query")
app.include_router(profile_router, prefix="/datasets")
app.include_router(ai_router, prefix="/ai")


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Data Copilot",
        "raw_data_dir": str(RAW_DATA_DIR),
        "processed_data_dir": str(PROCESSED_DATA_DIR),
    }


@app.get("/health")
def health():
    return {"status": "ok"}