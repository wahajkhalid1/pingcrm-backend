from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Contact as ContactModel, Organization as OrganizationModel
from schemas import ContactCreate, Contact as ContactSchema, OrganizationCreate, Organization as OrganizationSchema

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Organization CRUD
@app.post("/organizations/", response_model=OrganizationSchema)
def create_organization(organization: OrganizationCreate, db: Session = Depends(get_db)):
    db_organization = OrganizationModel(**organization.dict())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

@app.get("/organizations/", response_model=list[OrganizationSchema])
def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    organizations = db.query(OrganizationModel).offset(skip).limit(limit).all()
    return organizations

@app.get("/organizations/{organization_id}", response_model=OrganizationSchema)
def read_organization(organization_id: int, db: Session = Depends(get_db)):
    organization = db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@app.put("/organizations/{organization_id}", response_model=OrganizationSchema)
def update_organization(organization_id: int, organization: OrganizationCreate, db: Session = Depends(get_db)):
    db_organization = db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).first()
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    for key, value in organization.dict().items():
        setattr(db_organization, key, value)
    db.commit()
    db.refresh(db_organization)
    return db_organization

@app.delete("/organizations/{organization_id}")
def delete_organization(organization_id: int, db: Session = Depends(get_db)):
    db_organization = db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).first()
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.delete(db_organization)
    db.commit()
    return {"ok": True}

# Contact CRUD
@app.post("/contacts/", response_model=ContactSchema)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = ContactModel(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/", response_model=list[ContactSchema])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    organization_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(ContactModel)
    if search:
        query = query.filter(
            ContactModel.first_name.ilike(f"%{search}%") |
            ContactModel.last_name.ilike(f"%{search}%") |
            ContactModel.email.ilike(f"%{search}%")
        )
    if organization_id:
        query = query.filter(ContactModel.organization_id == organization_id)
    contacts = query.offset(skip).limit(limit).all()
    return contacts

@app.get("/contacts/{contact_id}", response_model=ContactSchema)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactModel).filter(ContactModel.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=ContactSchema)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(ContactModel).filter(ContactModel.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(ContactModel).filter(ContactModel.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"ok": True}
