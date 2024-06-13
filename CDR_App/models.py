from database import Base
from sqlalchemy import Column, Integer, String

class Contacts(Base): # Contacts Table
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    phonenumber = Column(String)
    email = Column(String)

