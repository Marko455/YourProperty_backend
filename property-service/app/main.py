from fastapi import FastAPI
from routes import router

app = FastAPI(title="Property Service")

app.include_router(router)
