from fastapi import status


def create_programme_for_course(client):
    payload = {
        "codeProgramme": "PRG-COURSE",
        "nomProgramme": "Programme pour Cours",
    }
    resp = client.post("/programmes/", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()["id"]


def test_create_course_ok(client):
    programme_id = create_programme_for_course(client)

    payload = {
        "codeCours": "CRS-001",
        "titreCours": "Cours Test",
        "programme_id": programme_id,
    }

    resp = client.post("/cours/", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()

    assert data["codeCours"] == payload["codeCours"]
    assert data["titreCours"] == payload["titreCours"]
    assert data["programme_id"] == programme_id
    assert data["id"] is not None
    assert data["dateCreation"] is not None


def test_create_course_unknown_programme(client):
    payload = {
        "codeCours": "CRS-UNKNOWN",
        "titreCours": "Cours Orphelin",
        "programme_id": 999999,  # n'existe pas
    }

    resp = client.post("/cours/", json=payload)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    data = resp.json()
    assert "Programme not found" in data["detail"]


def test_create_course_duplicate_code(client):
    programme_id = create_programme_for_course(client)

    payload = {
        "codeCours": "CRS-DUP",
        "titreCours": "Cours Dup 1",
        "programme_id": programme_id,
    }

    # premier OK
    resp1 = client.post("/cours/", json=payload)
    assert resp1.status_code == status.HTTP_201_CREATED

    # deuxième doit échouer
    resp2 = client.post("/cours/", json=payload)
    assert resp2.status_code == status.HTTP_400_BAD_REQUEST
    data = resp2.json()
    assert "already exists" in data["detail"]
