from fastapi import FastAPI
from user_service.app.api.routes import router

app = FastAPI(title="User Service")
app.include_router(router)
