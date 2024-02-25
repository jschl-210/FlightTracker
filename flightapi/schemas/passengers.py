from typing import Optional

from pydantic import BaseModel, Json


class PassengersBase(BaseModel):
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
