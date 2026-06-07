from pathlib import Path
from typing import Any

from sample_mcp import server


def test_sample_mcp_does_not_import_sample_api() -> None:
    source = Path(server.__file__).read_text(encoding="utf-8")

    assert "sample_api" not in source


def test_list_items_uses_http_api(monkeypatch) -> None:
    calls: list[tuple[str, str, dict[str, Any] | None]] = []

    def fake_request_json(
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> list[dict[str, str | int]]:
        calls.append((method, path, json))
        return [{"id": 1, "name": "hello", "description": "A friendly example item."}]

    monkeypatch.setattr(server, "_request_json", fake_request_json)

    assert server.list_items() == [
        {"id": 1, "name": "hello", "description": "A friendly example item."}
    ]
    assert calls == [("GET", "/items", None)]


def test_create_item_uses_http_api(monkeypatch) -> None:
    calls: list[tuple[str, str, dict[str, Any] | None]] = []

    def fake_request_json(
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> dict[str, str | int]:
        calls.append((method, path, json))
        return {"id": 3, "name": "new", "description": "Created over HTTP."}

    monkeypatch.setattr(server, "_request_json", fake_request_json)

    assert server.create_item("new", "Created over HTTP.") == {
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
