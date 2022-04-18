import unicodedata

from pydantic import BaseModel


class Player(BaseModel):
    name: str
    level: int
    vocation: str
    details: str

    def __str__(self):
        return f"{unicodedata.normalize('NFKD', self.name)} - {self.vocation_initials()} (Lvl: {self.level})"

    def vocation_initials(self):
        initials = {
            "Elite Knight": "EK",
            "Master Sorcerer": "MS",
            "Elder Druid": "ED",
            "Royal Paladin": "RP",
        }

        for k, v in initials.items():
            if self.vocation in k:
                return v
