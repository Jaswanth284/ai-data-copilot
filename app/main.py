from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from app.api.routes.upload import router as upload_router
from app.api.routes.query import router as query_router
from app.api.routes.profile import router as profile_router
from app.api.routes.ai import router as ai_router
from app.api.routes.rag import router as rag_router

app = FastAPI(title="AI Data Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/datasets")
app.include_router(query_router, prefix="/query")
app.include_router(profile_router, prefix="/datasets")
app.include_router(ai_router, prefix="/ai")
app.include_router(rag_router, prefix="/rag")


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