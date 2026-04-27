from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.predict import router

app = FastAPI(
    title   = "Indian Railways Prediction API",
    version = "1.0.0"
)

#
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "running", "message": "Railway Prediction API is live"}