from fastapi import FastAPI
from app.routes.listings import router

app = FastAPI(title="Listing Service")
app.include_router(router, prefix="/listings")
