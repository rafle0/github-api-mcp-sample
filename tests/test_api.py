import httpx
import pytest

from sample_api.main import app


def _api_client() -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://testserver")


@pytest.mark.anyio
async def test_health() -> None:
    async with _api_client() as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_list_items() -> None:
    async with _api_client() as client:
        response = await client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) >= 2


@pytest.mark.anyio
async def test_create_and_get_item() -> None:
    async with _api_client() as client:
        create_response = await client.post(
            "/items",
            json={"name": "github", "description": "Created from the sample API."},
        )

        assert create_response.status_code == 201
        created = create_response.json()

        get_response = await client.get(f"/items/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "github"
