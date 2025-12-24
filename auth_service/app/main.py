from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Auth Service")
app.include_router(router)
