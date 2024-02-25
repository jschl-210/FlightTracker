from pydantic import BaseModel


class APIConfig(BaseModel):
    root_path: str


class Config(BaseModel):
    api: APIConfig
