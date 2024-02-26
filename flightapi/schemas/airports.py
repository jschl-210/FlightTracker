from typing import Optional

from pydantic import BaseModel, Json


class AirportsBase(BaseModel):
    """
    Base model for airports.

    Args:
        code (Optional[str]): IATA airport code.
        name (Optional[str]): Airport name.
        city (Optional[str]): City name.
        country (Optional[str]): Country name.
    """
    code: Optional[str]
    name: Optional[str]
    city: Optional[str]
    country: Optional[str]


class AirportsCreate(AirportsBase):
    pass


class Airports(AirportsBase):
    """
    This class represents an airport.

    Args:
        id (int): The unique id of the airport.
        code (Optional[str]): IATA airport code.
        name (Optional[str]): Airport name.
        city (Optional[str]): City name.
        country (Optional[str]): Country name.
    """
    id: int

    class Config:
        """
        This class configures the Airports model.

        Args:
            from_attributes (bool): Whether to initialize the model from the attributes. Defaults to True.
        """
        from_attributes = True
