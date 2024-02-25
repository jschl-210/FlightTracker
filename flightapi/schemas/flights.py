from typing import Optional

from pydantic import BaseModel, Json


class FlightsBase(BaseModel):
    flight_status: Optional[str]
    flight_number: Optional[str]
    available_seats: Optional[str]
    departure_airport_id: int
    arrival_airport_id: int
    departure_date: str
    arrival_date: str
    duration: int
    fare: float


class FlightsCreate(FlightsBase):
    pass


class Flights(FlightsBase):
    id: int


class FlightsUpdate(BaseModel):
    flight_status: Optional[str]
    flight_number: Optional[str]
    available_seats: Optional[str]
    departure_airport_id: int
    arrival_airport_id: int
    departure_date: str
    arrival_date: str
    duration: int
    fare: float

    class Config:
        from_attributes = True
