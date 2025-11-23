from fastapi import status


def test_create_programme_ok(client):
    payload = {
        "codeProgramme": "PRG-001",
        "nomProgramme": "Programme Test",
        # les autres champs sont optionnels
    }

    resp = client.post("/programmes/", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()

    assert data["codeProgramme"] == payload["codeProgramme"]
    assert data["nomProgramme"] == payload["nomProgramme"]
    assert "id" in data
    assert data["id"] is not None
    # dateCreation ne doit pas être null si ton modèle est bien configuré
    assert data["dateCreation"] is not None


def test_create_programme_duplicate_code(client):
    payload = {
        "codeProgramme": "PRG-DUP",
        "nomProgramme": "Programme Dup1",
    }

    # premier OK
    resp1 = client.post("/programmes/", json=payload)
    assert resp1.status_code == status.HTTP_201_CREATED

    # second doit échouer
    resp2 = client.post("/programmes/", json=payload)
    assert resp2.status_code == status.HTTP_400_BAD_REQUEST
    data = resp2.json()
    assert "already exists" in data["detail"]


def test_get_programme_by_id(client):
    # on crée un programme
    payload = {
        "codeProgramme": "PRG-GET",
        "nomProgramme": "Programme Get",
    }
    resp = client.post("/programmes/", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    prog = resp.json()

    resp_get = client.get(f"/programmes/{prog['id']}")
    assert resp_get.status_code == status.HTTP_200_OK
    data = resp_get.json()
    assert data["id"] == prog["id"]
    assert data["codeProgramme"] == "PRG-GET"


def test_delete_programme(client):
    payload = {
        "codeProgramme": "PRG-DEL",
        "nomProgramme": "Programme Delete",
    }
    resp = client.post("/programmes/", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    prog_id = resp.json()["id"]

    resp_del = client.delete(f"/programmes/{prog_id}")
    assert resp_del.status_code == status.HTTP_204_NO_CONTENT

    resp_get = client.get(f"/programmes/{prog_id}")
    assert resp_get.status_code == status.HTTP_404_NOT_FOUND
