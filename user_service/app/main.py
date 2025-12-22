from fastapi import FastAPI
from app.routes.users import router

app = FastAPI(title="User Service")
app.include_router(router, prefix="/users")
