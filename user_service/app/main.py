from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="User Service")
app.include_router(router)
