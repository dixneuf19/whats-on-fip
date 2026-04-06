from pydantic import BaseModel


class Track(BaseModel):
    title: str
    album: str | None = None
    artist: str
    year: int | None = None
    label: str | None = None
    musical_kind: str | None = None
    external_urls: dict[str, str] = {}
    cover_url: str | None = None

    def __str__(self) -> str:
        return self.title + (f" ({self.year})" if self.year else "") + f" - {self.artist}"


class Station(BaseModel):
    name: str


class APIStatus(BaseModel):
    code: int
    message: str | None = None


class Message(BaseModel):
    message: str
