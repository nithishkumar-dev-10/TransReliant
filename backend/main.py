from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

@app.get("/health")
async def health():
    return {"status": "running", "message": "Railway Prediction API is live"}

# Serve the frontend (index.html) at the root URL.
# Must be mounted LAST — StaticFiles at "/" would otherwise shadow /api and /health.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")