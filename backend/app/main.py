from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, select
from typing import List

from .database import engine, get_session
from .models import InventoryItem, InventoryItemCreate, InventoryItemRead, InventoryItemUpdate
from . import crud

app = FastAPI(title="Inventarverwaltung")

# CORS für Vue.js Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Tables werden durch database/init.sql erstellt
    pass


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items", response_model=InventoryItemRead)
def create_item(item: InventoryItemCreate, session=Depends(get_session)):
    return crud.create_item(session, item)


@app.get("/items", response_model=List[InventoryItemRead])
def list_items(location: str | None = None, session=Depends(get_session)):
    return crud.get_items(session, location)


@app.get("/items/{item_id}", response_model=InventoryItemRead)
def get_item(item_id: int, session=Depends(get_session)):
    db_item = crud.get_item(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.put("/items/{item_id}", response_model=InventoryItemRead)
def update_item(item_id: int, item: InventoryItemUpdate, session=Depends(get_session)):
    updated = crud.update_item(session, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, session=Depends(get_session)):
    ok = crud.delete_item(session, item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
