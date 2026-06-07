from pathlib import Path
from typing import Any

import httpx
import pytest

from sample_mcp import server


def test_sample_mcp_does_not_import_sample_api() -> None:
    source = Path(server.__file__).read_text(encoding="utf-8")

    assert "sample_api" not in source


@pytest.mark.anyio
async def test_list_items_uses_http_api(monkeypatch) -> None:
    calls: list[tuple[str, str, dict[str, Any] | None]] = []

    async def fake_request_json(
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> list[dict[str, str | int]]:
        calls.append((method, path, json))
        return [{"id": 1, "name": "hello", "description": "A friendly example item."}]

    monkeypatch.setattr(server, "_request_json", fake_request_json)

    assert await server.list_items() == [
        {"id": 1, "name": "hello", "description": "A friendly example item."}
    ]
    assert calls == [("GET", "/items", None)]


@pytest.mark.anyio
async def test_create_item_uses_http_api(monkeypatch) -> None:
    calls: list[tuple[str, str, dict[str, Any] | None]] = []

    async def fake_request_json(
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> dict[str, str | int]:
        calls.append((method, path, json))
        return {"id": 3, "name": "new", "description": "Created over HTTP."}

    monkeypatch.setattr(server, "_request_json", fake_request_json)

    assert await server.create_item("new", "Created over HTTP.") == {
        "id": 3,
        "name": "new",
        "description": "Created over HTTP.",
    }
    assert calls == [
        (
            "POST",
            "/items",
            {"name": "new", "description": "Created over HTTP."},
        )
    ]


@pytest.mark.anyio
async def test_get_client_reuses_lazy_singleton(monkeypatch) -> None:
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json=[]))
    created: list[httpx.AsyncClient] = []

    def create_client() -> httpx.AsyncClient:
        client = httpx.AsyncClient(transport=transport)
        created.append(client)
        return client

    monkeypatch.setattr(server, "_client", None)
    monkeypatch.setattr(server, "_create_client", create_client)

    assert server._get_client() is server._get_client()
    assert len(created) == 1

    await server._close_client()


@pytest.mark.anyio
async def test_close_client_resets_lazy_singleton(monkeypatch) -> None:
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json=[]))
    client = httpx.AsyncClient(transport=transport)

    monkeypatch.setattr(server, "_client", client)

    await server._close_client()

    assert server._client is None
    assert client.is_closed
