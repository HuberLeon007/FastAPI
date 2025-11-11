from typing import Optional
from sqlmodel import SQLModel, Field


class InventoryItemBase(SQLModel):
    name: str
    category: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    assigned_to: Optional[str] = None


class InventoryItem(InventoryItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemRead(InventoryItemBase):
    id: int


class InventoryItemUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    assigned_to: Optional[str] = None
