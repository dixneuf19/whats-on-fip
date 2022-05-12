from typing import Dict, Optional

from pydantic import BaseModel


class Track(BaseModel):
    title: str
    album: Optional[str]
    artist: str
    year: Optional[int]
    label: Optional[str]
    musical_kind: Optional[str]
    external_urls: Dict[str, str] = {}
    cover_url: Optional[str]

    def __str__(self) -> str:
        return self.title + f" ({self.year})" if self.year else "" + f" - {self.artist}"


class Station(BaseModel):
    name: str


class APIStatus(BaseModel):
    code: int
    message: Optional[str]


class Message(BaseModel):
    message: str
