from typing import List, Optional, Dict

from pydantic import BaseModel


class Track(BaseModel):
    title: str
    album: str
    artist: str
    year: Optional[int]
    label: Optional[str]
    musical_kind: Optional[str]
    external_urls: Dict[str, str] = {}
    cover_url: Optional[str]


class Station(BaseModel):
    name: str


class APIStatus(BaseModel):
    code: int
    message: Optional[str]


class Message(BaseModel):
    message: str
