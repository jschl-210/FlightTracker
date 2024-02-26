from typing import Optional

from pydantic import BaseModel, Json


class PassengersBase(BaseModel):
    """
    Base model for passengers.

    Args:
        flight_id (int): Flight ID.
        first_name (str): First name.
        last_name (str): Last name.
        date_of_birth (str): Date of birth.
        passport_number (str): Passport number.
    """
    flight_id: int
    first_name: str
    last_name: str
    date_of_birth: str
    passport_number: str


class PassengersCreate(PassengersBase):
    pass


class Passengers(PassengersBase):
    id: int


class PassengersUpdate(BaseModel):
    flight_id: int
    first_name: str
    last_name: str
    date_of_birth: str
    passport_number: str

    class Config:
        from_attributes = True
