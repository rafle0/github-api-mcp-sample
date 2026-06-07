from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from sample_api.store import store


mcp = FastMCP("sample-api")


@mcp.tool()
def list_items() -> list[dict[str, str | int]]:
    """List all sample API items."""
    return [item.__dict__ for item in store.list_items()]


@mcp.tool()
def get_item(item_id: int) -> dict[str, str | int]:
    """Get one sample API item by id."""
    item = store.get_item(item_id)
    if item is None:
        raise ValueError(f"Item {item_id} was not found")
    return item.__dict__


@mcp.tool()
def create_item(name: str, description: str) -> dict[str, str | int]:
    """Create a sample API item."""
    item = store.create_item(name=name, description=description)
    return item.__dict__


if __name__ == "__main__":
    mcp.run()
