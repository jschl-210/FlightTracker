from typing import Optional

from pydantic import BaseModel, Json


class AirlinesBase(BaseModel):
    code: Optional[str]
    name: Optional[str]
    alliance: Optional[str]


class AirlinesCreate(AirlinesBase):
    pass


class Airlines(AirlinesBase):
    id: int

    class Config:
        from_attributes = True
