from fastapi import FastAPI
from routes import router

app = FastAPI(title="Inquiry Service")

app.include_router(router)
