# Part 1 — Imports
# FastAPI app and the predict router
from fastapi import FastAPI
from api.routes.predict import router


# Creates the main FastAPI application instance
app = FastAPI(
    title    = "Indian Railways Prediction API",
    version  = "1.0.0"
)


# Attaches the predict route to the app under /api prefix
app.include_router(router, prefix="/api")


# Part 4 — Root health check
# Simple GET to confirm server is running
@app.get("/")
async def root():
    return {"status": "running", "message": "Railway Prediction API is live"}