from fastapi import FastAPI
from app.routes.auth import router

app = FastAPI(title="Auth Service")
app.include_router(router, prefix="/auth")
