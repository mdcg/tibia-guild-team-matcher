import unicodedata

from pydantic import BaseModel


class Player(BaseModel):
    name: str
    level: int
    vocation: str
    details: str

    def __str__(self):
        """Special method to represent Player object in string.

        Returns:
            str: Simple formatting with Player Name, vocation initials and
            level.
        """
        return f"{unicodedata.normalize('NFKD', self.name)} - {self.vocation_initials()} (Lvl: {self.level})"

    def vocation_initials(self):
        """In Tibia, vocations are called by their initials. Basically, here we
        have a method that translates the player's vocation to their respective
        initials.

        Returns:
            str: Player vocation initials.
        """
        initials = {
            "Elite Knight": "EK",
            "Master Sorcerer": "MS",
            "Elder Druid": "ED",
            "Royal Paladin": "RP",
        }

        for k, v in initials.items():
            if self.vocation in k:
                return v
