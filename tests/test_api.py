from fastapi.testclient import TestClient

from sample_api.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_items() -> None:
    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_create_and_get_item() -> None:
    create_response = client.post(
        "/items",
        json={"name": "github", "description": "Created from the sample API."},
    )

    assert create_response.status_code == 201
    created = create_response.json()

    get_response = client.get(f"/items/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "github"
