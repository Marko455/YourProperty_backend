from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Listing Service")
app.include_router(router)
