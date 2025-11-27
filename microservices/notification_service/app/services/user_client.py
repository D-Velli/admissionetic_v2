import httpx
from app.core.config import USER_SERVICE_URL
import logging

logger = logging.getLogger(__name__)


def get_user_details(user_id: int) -> str | None:
    print("JE SUIS ICI")
    if not USER_SERVICE_URL:
        logger.error("USER_SERVICE_URL non configurée")
        return None

    url = f"{USER_SERVICE_URL}/users/{user_id}"
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(url)
        if resp.status_code != 200:
            logger.warning("User %s non trouvé: %s", user_id, resp.text)
            return None
        data = resp.json()
        print(f"Data : {data}")
        return data.get("email")
    except Exception:
        logger.exception("Erreur lors de l'appel user_service")
        return None
