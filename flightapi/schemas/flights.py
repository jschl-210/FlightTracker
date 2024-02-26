from typing import Optional

from pydantic import BaseModel, Json


class FlightsBase(BaseModel):
    """
    The base model for all flights.

    Args:
        flight_status (Optional[str]): The current status of the flight.
        flight_number (Optional[str]): The flight number of the flight.
        available_seats (Optional[str]): The number of available seats on the flight.
        departure_airport_id (int): The ID of the departure airport.
        arrival_airport_id (int): The ID of the arrival airport.
        departure_date (str): The date of the departure of the flight.
        arrival_date (str): The date of the arrival of the flight.
        duration (int): The duration of the flight in minutes.
        fare (float): The fare of the flight.
    """
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
