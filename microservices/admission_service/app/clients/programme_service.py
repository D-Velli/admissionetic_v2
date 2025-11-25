import requests
from fastapi import HTTPException, status

from app.core.config import PROGRAMME_SERVICE_URL


# M'assurer que le programme dont l'utilisateur veut faire une admission existe
def ensure_programme_exists(programme_id: int) -> None:
    url = f"{PROGRAMME_SERVICE_URL}/programmes/{programme_id}"
    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Impossible de contacter programme_service",
        )

    if resp.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Programme inexistant.",
        )
    if resp.status_code >= 500:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erreur de programme_service",
        )


# M'assurer que le cours dont l'utilisateur veut faire une admission existe
def ensure_cours_exists(cours_id: int) -> None:
    url = f"{PROGRAMME_SERVICE_URL}/cours/{cours_id}"  # adapte au vrai endpoint
    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Impossible de contacter programme_service",
        )

    if resp.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cours inexistant.",
        )
    if resp.status_code >= 500:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Erreur de programme_service",
        )
