from fastapi import FastAPI
from backend.api.routes.predict import router

app = FastAPI(
    title   = "Indian Railways Prediction API",
    version = "1.0.0"
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "running", "message": "Railway Prediction API is live"}