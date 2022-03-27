from pydantic import BaseModel


class Player(BaseModel):
    name: str
    level: int
    vocation: str
    details: str
