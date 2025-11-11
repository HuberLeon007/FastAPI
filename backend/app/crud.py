from typing import List, Optional
from sqlmodel import Session, select

from .models import InventoryItem, InventoryItemCreate, InventoryItemUpdate


def get_item(session: Session, item_id: int) -> Optional[InventoryItem]:
    return session.get(InventoryItem, item_id)


def get_items(session: Session, location: Optional[str] = None) -> List[InventoryItem]:
    statement = select(InventoryItem)
    if location:
        statement = statement.where(InventoryItem.location == location)
    return session.exec(statement).all()


def create_item(session: Session, item_create: InventoryItemCreate) -> InventoryItem:
    item = InventoryItem.from_orm(item_create)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def update_item(session: Session, item_id: int, item_update: InventoryItemUpdate) -> Optional[InventoryItem]:
    item = get_item(session, item_id)
    if not item:
        return None
    update_data = item_update.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(item, k, v)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def delete_item(session: Session, item_id: int) -> bool:
    item = get_item(session, item_id)
    if not item:
        return False
    session.delete(item)
    session.commit()
    return True
