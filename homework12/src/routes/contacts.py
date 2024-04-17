from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.repository.contacts import (get_contacts, create_contact, get_contact, update_contact, delete_contact,
                                     get_contacts_by_search, get_birthdays)
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from typing import List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact_endpoint(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact)


@router.get("/", response_model=List[ContactResponse])
def read_contacts(db: Session = Depends(get_db)):
    return get_contacts(db)


@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    return get_contact(db, contact_id)


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact_endpoint(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = update_contact(db, contact_id, contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}")
def delete_contact_endpoint(contact_id: int, db: Session = Depends(get_db)):
    if not delete_contact(db, contact_id):
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}


@router.get("/search/")
def search_contact_endpoint(query: str, db: Session = Depends(get_db)):
    contacts = get_contacts_by_search(db, query)
    return contacts


@router.get("/birthdays/")
def get_birthdays_endpoint(db: Session = Depends(get_db)):
    contacts = get_birthdays(db)
    return contacts
