from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
from .events.payment_events import start_payment_events_listener
from contextlib import asynccontextmanager

import logging

from .routes import admissions

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting REDIS admission_service...")

    # --------- STARTUP ----------
    start_payment_events_listener()  # <- démarre ton thread Redis
    # tu peux log ici si tu veux
    yield
    # --------- SHUTDOWN ----------
    # si un jour tu veux arrêter proprement le listener, tu le feras ici


app = FastAPI(title="Admission Service", lifespan=lifespan)


# ---------- CORS ----------

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # ajoute ici ton front en prod, ex:
    # "https://front.monsite.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # ou ["*"] si tu t'en fous en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- ROUTERS ----------

app.include_router(admissions.router)


# --------- DEMARRAGE -----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8002, reload=True)
    
    

# ---------- GESTION GLOBALE DES ERREURS ----------

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(
        f"HTTP {exc.status_code} - {exc.detail} - path={request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(
        f"Validation error - path={request.url.path} - errors={exc.errors()}"
    )
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(
        f"IntegrityError - path={request.url.path} - {exc}"
    )
    # on ne connaît pas le détail exact → message générique
    return JSONResponse(
        status_code=400,
        content={"detail": "Database integrity error"},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        f"Unhandled error - path={request.url.path}"
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )