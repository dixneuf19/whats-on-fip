import json
import os
from typing import Any, List

import requests
from engineio import packet

from whats_on_fip.models import Track

RADIO_5050_URL = os.getenv(
    "RADIO_5050_URL", "https://www.radio5050.com/realtime/socket.io/"
)
COMMON_PARAMS = {"EIO": "4", "transport": "polling"}


def _parse_response(res: requests.Response) -> List[Any]:
    encoded_packets = res.content.split(b"\x1e")
    packets = [
        packet.Packet(encoded_packet=encoded_packet)
        for encoded_packet in encoded_packets
    ]
    return [_parse_packet(p) for p in packets]


def _parse_packet(pack: packet) -> Any:
    txt = pack.data.decode("utf-8")
    i = 0
    while txt[i].isnumeric():
        i += 1

    return json.loads(txt[i:])


def get_current_song() -> Track:
    # 1. Get a SID
    res = requests.get(RADIO_5050_URL, params=COMMON_PARAMS)
    res.raise_for_status()
    sid = _parse_response(res)[0]["sid"]

    common_params_with_sid = {"sid": sid, **COMMON_PARAMS}

    # 2. Connect to namespace
    res = requests.post(
        RADIO_5050_URL, params=common_params_with_sid, data="40".encode("utf-8")
    )
    res.raise_for_status()
    if not res.content.decode("utf-8") == "ok":
        raise Exception("failed to connect to namespace")

    # 3. Emit a subscribe event to nowplaying-room
    res = requests.post(
        RADIO_5050_URL,
        params=common_params_with_sid,
        data='42["subscribe","nowplaying-room"]'.encode("utf-8"),
    )
    res.raise_for_status()
    if not res.content.decode("utf-8") == "ok":
        raise Exception("failed suscribe to nowplaying-room")

    # 4. Get the value
    res = requests.get(RADIO_5050_URL, params=common_params_with_sid)
    res.raise_for_status()

    song = _parse_response(res)[-1][-1]["history"][0]

    return Track(album="", **song)
