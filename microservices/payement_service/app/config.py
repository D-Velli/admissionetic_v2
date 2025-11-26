import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env_payement")

DATABASE_URL = os.getenv("DATABASE_URL")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

SECRET_KEY = os.getenv("SECRET_KEY")            # pour JWT
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not all([DATABASE_URL, STRIPE_SECRET_KEY, SECRET_KEY]):
    raise RuntimeError("Config manquante dans .env_payement")
