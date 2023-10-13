from typing import Protocol

from whats_on_fip.models import Track


class Radio(Protocol):
    def get_current_track(self) -> Track:
        ...
