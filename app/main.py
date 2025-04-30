from fastapi import FastAPI
from app.auth import routes as auth_routes

app = FastAPI()

app.include_router(auth_routes.router)
