from __future__ import annotations

import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sample-api")
_client: httpx.AsyncClient | None = None


def _api_base_url() -> str:
    return os.environ.get("SAMPLE_API_BASE_URL", "http://127.0.0.1:8000")


def _create_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=_api_base_url(),
        timeout=httpx.Timeout(10.0, connect=3.0),
        limits=httpx.Limits(
            max_connections=20,
            max_keepalive_connections=10,
            keepalive_expiry=30.0,
        ),
    )


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = _create_client()
    return _client


async def _close_client() -> None:
    global _client
    if _client is None:
        return

    await _client.aclose()
    _client = None


async def _request_json(
    method: str,
    path: str,
    *,
    json: dict[str, Any] | None = None,
) -> Any:
    response = await _get_client().request(method, path, json=json)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise ValueError(
            f"API request failed: {response.status_code} {response.text}"
        ) from exc

    return response.json()


@mcp.tool()
async def list_items() -> list[dict[str, str | int]]:
    """List all sample API items."""
    return await _request_json("GET", "/items")


@mcp.tool()
async def get_item(item_id: int) -> dict[str, str | int]:
    """Get one sample API item by id."""
    return await _request_json("GET", f"/items/{item_id}")


@mcp.tool()
async def create_item(name: str, description: str) -> dict[str, str | int]:
    """Create a sample API item."""
    return await _request_json(
        "POST",
        "/items",
        json={"name": name, "description": description},
    )


if __name__ == "__main__":
    mcp.run()
