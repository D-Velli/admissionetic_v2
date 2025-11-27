import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env_notification")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", "no-reply@example.com")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
ADMISSION_SERVICE_URL = os.getenv("ADMISSION_SERVICE_URL")

print(f"Base_dir : {BASE_DIR}")
print(f"user_url : {USER_SERVICE_URL}")
