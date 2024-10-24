from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from models import Location
import os

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LocationInput(BaseModel):
    latitude: float
    longitude: float
    timestamp: str

@app.get("/")
async def root():
    return {"message": "Location Tracking API is running"}

@app.post("/update_location")
async def create_location(location: LocationInput, db: Session = Depends(get_db)):
    try:
        new_location = Location(
            latitude=location.latitude,
            longitude=location.longitude,
            timestamp=location.timestamp
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        return {"message": "Location updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/locations/")
async def get_locations(db: Session = Depends(get_db)):
    try:
        return db.query(Location).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)