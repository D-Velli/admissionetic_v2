import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env_admission")

PROGRAMME_SERVICE_URL = os.getenv("PROGRAMME_SERVICE_URL")
REDIS_URL = os.getenv("REDIS_URL")