from fastapi import FastAPI
from listing_service.app.api.routes import router

app = FastAPI(title="Listing Service")
app.include_router(router)
