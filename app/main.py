from fastapi import FastAPI
from .routes import instagram_routes

app = FastAPI()
app.include_router(instagram_routes.router, prefix="/api")