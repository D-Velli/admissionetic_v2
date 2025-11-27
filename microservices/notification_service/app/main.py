import logging
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.events.payment_event import start_payment_events_listener

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification_service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Démarrage de notification_service...")
    start_payment_events_listener()
    yield
    logger.info("🛑 Arrêt de notification_service...")


app = FastAPI(title="Notification Service", lifespan=lifespan)

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


@app.get("/health")
def health():
    return {"status": "ok"}


# --------- DEMARRAGE -----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8004, reload=True)
