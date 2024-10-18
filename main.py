# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import Base, engine, get_db
from .models import Location

Base.metadata.create_all(bind=engine)

app = FastAPI()
class LocationInput(BaseModel):
    latitude: float
    longitude: float
    timestamp: str  


@app.post("/update_location")
async def create_location(location: LocationInput, db: Session = Depends(get_db)):
    new_location = Location(
        latitude=location.latitude,
        longitude=location.longitude,
        timestamp=location.timestamp  
    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return {"message": "Location updated successfully"}


@app.get("/locations/")
async def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()
