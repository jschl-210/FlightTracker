from typing import Optional

from pydantic import BaseModel, Json


class AirlinesBase(BaseModel):
    """
    Base model for airlines data.

    Args:
        code (str, optional): IATA airline code.
        name (str, optional): Airline name.
        alliance (str, optional): Airline alliance.
    """
    code: Optional[str]
    name: Optional[str]
    alliance: Optional[str]


class AirlinesCreate(AirlinesBase):
    pass


class Airlines(AirlinesBase):
    """
        Pydantic model for airlines data.

        Args:
            code (str, optional): IATA airline code.
            name (str, optional): Airline name.
            alliance (str, optional): Airline alliance.
            id (int): Unique record identifier.

        Returns:
            Airlines: Pydantic model.
        """
    id: int

    class Config:
        from_attributes = True
