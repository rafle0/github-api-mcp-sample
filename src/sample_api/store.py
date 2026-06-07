from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class Item:
    id: int
    name: str
    description: str


class ItemStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._items: dict[int, Item] = {
            1: Item(id=1, name="hello", description="A friendly example item."),
            2: Item(id=2, name="mcp", description="An item exposed through MCP tools."),
        }
        self._next_id = 3

    def list_items(self) -> list[Item]:
        with self._lock:
            return list(self._items.values())

    def get_item(self, item_id: int) -> Item | None:
        with self._lock:
            return self._items.get(item_id)

    def create_item(self, name: str, description: str) -> Item:
        with self._lock:
            item = Item(id=self._next_id, name=name, description=description)
            self._items[item.id] = item
            self._next_id += 1
            return item


store = ItemStore()
