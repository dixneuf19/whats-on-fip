from typing import Dict, Optional

from pydantic import BaseModel


class Track(BaseModel):
    title: str
    album: Optional[str] = None
    artist: str
    year: Optional[int] = None
    label: Optional[str] = None
    musical_kind: Optional[str] = None
    external_urls: Dict[str, str] = {}
    cover_url: Optional[str] = None

    def __str__(self) -> str:
        return self.title + f" ({self.year})" if self.year else "" + f" - {self.artist}"


class Station(BaseModel):
    name: str


class APIStatus(BaseModel):
    code: int
    message: Optional[str] = None


class Message(BaseModel):
    message: str
