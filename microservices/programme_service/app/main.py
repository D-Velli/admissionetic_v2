from fastapi import FastAPI
from .routes import programmes, cours

app = FastAPI(title="Programme Service")

app.include_router(programmes.router, prefix="/programmes", tags=["Programmes"])
app.include_router(cours.router, prefix="/cours", tags=["Cours"])
