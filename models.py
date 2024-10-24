
from sqlalchemy import Column, Integer, Float, String
from database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)  # Almacenamos la marca de tiempo como cadena
