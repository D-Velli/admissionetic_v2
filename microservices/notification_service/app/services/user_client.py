import httpx
from app.core.config import USER_SERVICE_URL, INTERNAL_API_TOKEN
import logging

logger = logging.getLogger(__name__)


def get_user_details(user_id: int) -> str | None:
    if not USER_SERVICE_URL:
        logger.error("USER_SERVICE_URL non configurée")
        return None

    url = f"{USER_SERVICE_URL}/users/{user_id}"
    headers = {"X-Internal-Token": INTERNAL_API_TOKEN}
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(url, headers=headers)
        if resp.status_code != 200:
            logger.warning("User %s non trouvé: %s", user_id, resp.text)
            return None
        data = resp.json()
        return data
    except Exception:
        logger.exception("Erreur lors de l'appel user_service")
        return None
