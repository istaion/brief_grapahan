from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List

import os
from .database import engine, get_db
from .models import Base, Client
from .schemas import ClientCreate, ClientRead

ROOT_PATH = os.getenv("ROOT_PATH", "")

app = FastAPI(title="Clients API", version="1.0.0", root_path=ROOT_PATH)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/clients", response_model=List[ClientRead])
def list_clients(db: Session = Depends(get_db)):
    clients = db.execute(select(Client).order_by(Client.id)).scalars().all()
    return clients

@app.get("/clients/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client

@app.post("/clients", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    existing = db.execute(select(Client).where(Client.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@app.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    db.delete(client)
    db.commit()
    return None
