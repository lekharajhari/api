from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory database simulation
contacts_db = []

# Contact model
class Contact(BaseModel):
    name: str
    number: str
    city: Optional[str] = None

# CRUD Operations

# 1. Create a contact
@app.post("/contacts/", response_model=Contact)
def create_contact(contact: Contact):
    # Check if contact already exists
    for c in contacts_db:
        if c.name == contact.name:
            raise HTTPException(status_code=400, detail="Contact with this name already exists")
    contacts_db.append(contact)
    return contact

# 2. Read all contacts
@app.get("/contacts/", response_model=List[Contact])
def get_contacts():
    return contacts_db

# 3. Read a contact by name
@app.get("/contacts/{name}", response_model=Contact)
def get_contact_by_name(name: str):
    for contact in contacts_db:
        if contact.name == name:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")

# 4. Update a contact
@app.put("/contacts/{name}", response_model=Contact)
def update_contact(name: str, updated_contact: Contact):
    for index, contact in enumerate(contacts_db):
        if contact.name == name:
            contacts_db[index] = updated_contact
            return updated_contact
    raise HTTPException(status_code=404, detail="Contact not found")

# 5. Delete a contact
@app.delete("/contacts/{name}", response_model=str)
def delete_contact(name: str):
    for index, contact in enumerate(contacts_db):
        if contact.name == name:
            contacts_db.pop(index)
            return f"Contact {name} deleted"
    raise HTTPException(status_code=404, detail="Contact not found")

# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)