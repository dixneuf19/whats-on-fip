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


class Radio(BaseModel):
    name: str
    url: str


FIP_RADIO = Radio(name="FIP", url="https://www.fip.fr")
MEUH_RADIO = Radio(name="Radiomeuh", url="https://www.radiomeuh.com/")
FIFTYFIFTY_RADIO = Radio(name="Radio5050", url="https://www.radio5050.com/")
FEELGOOD_RADIO = Radio(name="Radio FG - Feel Good", url="https://www.radiofg.com/")
