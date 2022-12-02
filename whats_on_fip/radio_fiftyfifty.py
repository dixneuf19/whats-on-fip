import json
import os
from typing import Any, List

import requests
from engineio import packet

from whats_on_fip.models import Track
from whats_on_fip.radio import Radio


class Radio5050(Radio):
    def __init__(self) -> None:
        self.url = os.getenv(
            "RADIO_5050_URL", "https://www.radio5050.com/realtime/socket.io/"
        )
        self.common_params = {"EIO": "4", "transport": "polling"}

    def __parse_response(self, res: requests.Response) -> List[Any]:
        encoded_packets = res.content.split(b"\x1e")
        packets = [
            packet.Packet(encoded_packet=encoded_packet)
            for encoded_packet in encoded_packets
        ]
        return [self.__parse_packet(p) for p in packets]

    def __parse_packet(self, pack: packet) -> Any:
        txt = pack.data.decode("utf-8")
        i = 0
        while txt[i].isnumeric():
            i += 1

        return json.loads(txt[i:])

    def get_current_track(self) -> Track:
        # 1. Get a SID
        res = requests.get(self.url, params=self.common_params)
        res.raise_for_status()
        sid = self.__parse_response(res)[0]["sid"]

        common_params_with_sid = {"sid": sid, **self.common_params}

        # 2. Connect to namespace
        res = requests.post(
            self.url, params=common_params_with_sid, data="40".encode("utf-8")
        )
        res.raise_for_status()
        if not res.content.decode("utf-8") == "ok":
            raise Exception("failed to connect to namespace")

        # 3. Emit a subscribe event to nowplaying-room
        res = requests.post(
            self.url,
            params=common_params_with_sid,
            data='42["subscribe","nowplaying-room"]'.encode("utf-8"),
        )
        res.raise_for_status()
        if not res.content.decode("utf-8") == "ok":
            raise Exception("failed suscribe to nowplaying-room")

        # 4. Get the value
        res = requests.get(self.url, params=common_params_with_sid)
        res.raise_for_status()

        song = self.__parse_response(res)[-1][-1]["history"][0]

        return Track(album="", **song)
