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
    """Retrieve every item currently stored by the sample HTTP API.

    Use this tool when the user asks to browse, inspect, or summarize the
    available sample items. It does not take any arguments. The result is a list
    of item objects, each containing `id`, `name`, and `description`.
    """
    return await _request_json("GET", "/items")


@mcp.tool()
async def get_item(item_id: int) -> dict[str, str | int]:
    """Retrieve one item from the sample HTTP API by numeric id.

    Use this tool when the user asks for details about a specific item and
    provides its `item_id`. The result contains the item's `id`, `name`, and
    `description`. If the API cannot find the item, this tool raises an error
    with the HTTP status and response body.
    """
    return await _request_json("GET", f"/items/{item_id}")


@mcp.tool()
async def create_item(name: str, description: str) -> dict[str, str | int]:
    """Create a new item through the sample HTTP API.

    Use this tool when the user wants to add a sample item. Provide a short
    `name` and a human-readable `description`. The API validates both fields
    and returns the created item with its generated numeric `id`.
    """
    return await _request_json(
        "POST",
        "/items",
        json={"name": name, "description": description},
    )


if __name__ == "__main__":
    mcp.run()
