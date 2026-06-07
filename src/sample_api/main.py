from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from sample_api.store import Item, store


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=240)


app = FastAPI(
    title="Sample API for MCP",
    summary="A tiny Python API that can also be exposed through MCP tools.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items", response_model=list[Item])
def list_items() -> list[Item]:
    return store.list_items()


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = store.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=Item, status_code=201)
def create_item(payload: ItemCreate) -> Item:
    return store.create_item(payload.name, payload.description)
