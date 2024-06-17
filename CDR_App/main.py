from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
import models
from models import Contacts
from database import SessionLocal, engine
from routers import auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ContactRequest(BaseModel):
    firstname: str
    lastname: str
    phonenumber: str
    email: str

class SuccessResponse(BaseModel):
    message: str

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_contacts(db: db_dependency):
    return db.query(Contacts).all()

@app.post("/contact", status_code=status.HTTP_201_CREATED)
async def new_contact(db: db_dependency, contact_request: ContactRequest):
    contact_model = Contacts(**contact_request.model_dump())

    db.add(contact_model)
    db.commit()
    return SuccessResponse(message="Contact created successfully!")

@app.put("/contact/{contact_id}", status_code=status.HTTP_200_OK)
async def edit_contact(db: db_dependency, contact_id: int, contact_request: ContactRequest):
    
    contact_model = db.query(Contacts).filter(Contacts.id == contact_id).first() # To change later to username

    if contact_model is None:
        raise HTTPException(status_code=404, detail="Contact not Found")

    contact_model.firstname =  contact_request.firstname
    contact_model.lastname = contact_request.lastname
    contact_model.phonenumber = contact_request.phonenumber
    contact_model.email = contact_request.email
    
    db.add(contact_model)
    db.commit()
    return SuccessResponse(message="Contact Successfully Updated!")

@app.delete("/contact/{contact_id}", status_code=status.HTTP_200_OK)
async def delete_contact(db: db_dependency, contact_id: int):
    contact_model = db.query(Contacts).filter(Contacts.id == contact_id).first()

    if contact_model is None:
        raise HTTPException(status_code=404, detail="Contact not Found")
    else:
        db.query(Contacts).filter(Contacts.id == contact_id).delete()
        db.commit()
        return SuccessResponse(message="Contact deleted successfully!")