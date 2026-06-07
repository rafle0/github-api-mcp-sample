from __future__ import annotations

import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sample-api")


def _api_base_url() -> str:
    return os.environ.get("SAMPLE_API_BASE_URL", "http://127.0.0.1:8000")


def _request_json(
    method: str,
    path: str,
    *,
    json: dict[str, Any] | None = None,
) -> Any:
    with httpx.Client(base_url=_api_base_url(), timeout=10.0) as client:
        response = client.request(method, path, json=json)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise ValueError(
            f"API request failed: {response.status_code} {response.text}"
        ) from exc

    return response.json()


@mcp.tool()
def list_items() -> list[dict[str, str | int]]:
    """List all sample API items."""
    return _request_json("GET", "/items")


@mcp.tool()
def get_item(item_id: int) -> dict[str, str | int]:
    """Get one sample API item by id."""
    return _request_json("GET", f"/items/{item_id}")


@mcp.tool()
def create_item(name: str, description: str) -> dict[str, str | int]:
    """Create a sample API item."""
    return _request_json(
        "POST",
        "/items",
        json={"name": name, "description": description},
    )


if __name__ == "__main__":
    mcp.run()
