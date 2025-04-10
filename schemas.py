from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    address: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    organization_id: int

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime
    organization: Organization
    class Config:
        from_attributes = True
