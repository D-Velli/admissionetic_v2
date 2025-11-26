import os
from dataclasses import dataclass
import httpx

ADMISSION_SERVICE_URL = os.getenv("ADMISSION_SERVICE_URL")

@dataclass
class AdmissionDTO:
    id: int
    user_id: int
    status: str
    amount: float
    currency: str = "cad"

def get_admission_or_raise(admission_id: int, token: str) -> AdmissionDTO:
    """
    Va chercher l'admission dans admission_service.
    Lève une exception si elle n'existe pas ou si autre erreur.
    """
    url = f"{ADMISSION_SERVICE_URL}/admissions/{admission_id}"
    headers = {"Authorization": f"Bearer {token}"}

    with httpx.Client(timeout=5.0) as client:
        resp = client.get(url, headers=headers)

    if resp.status_code == 404:
        # Admission inexistante
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admission not found",
        )
    if resp.status_code != 200:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admission n'est à toi la ooo",
        )

    data = resp.json()
    # adapte selon ton retour réel
    return AdmissionDTO(
        id=data["id"],
        user_id=data["user_id"],
        status=data["status"],
        amount=float(data["frais_admission"]),   # vient de AdmissionRead
        currency=data.get("currency", "cad"),    # par sécurité
    )
