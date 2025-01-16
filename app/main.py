from fastapi import FastAPI
from .routes import instagram_routes, user_routes, household_routes

app = FastAPI()

app.include_router(instagram_routes, prefix="/api")
app.include_router(user_routes, prefix="/api/users")
app.include_router(household_routes, prefix="/api/households")