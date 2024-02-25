from typing import Optional

from pydantic import BaseModel, Json


class AirportsBase(BaseModel):
    code: Optional[str]
    name: Optional[str]
    city: Optional[str]
    country: Optional[str]


class AirportsCreate(AirportsBase):
    pass


class Airports(AirportsBase):
    id: int

    class Config:
        from_attributes = True
