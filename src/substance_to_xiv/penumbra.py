# Modified PenumbraClient class from Yet Another Addon by Aleks (GPL-3.0).
# https://github.com/Arrenval/Yet-Another-Addon/blob/main/utils/penumbra.py

import json
import urllib.request as req
from urllib.error import URLError


class PenumbraClient:
    def __init__(self, base_url="http://localhost:42069/api"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        self.timeout = 2

    def _send(self, endpoint: str, data: dict | None = None) -> None:
        request = req.Request(
            url=f"{self.base_url}{endpoint}",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            req.urlopen(request, timeout=1)
            return "Penumbra redrawn succesfully."
        except URLError as e:
            return f"Penumbra not responding: {e}"
        except Exception as e:
            return f"Penumbra not responding: {e}"

    def redraw_self(self) -> None:
        return self._send("/redraw", {"ObjectTableIndex": 0, "Type": 0})

    def redraw_all(self) -> None:
        return self._send("/redrawAll")

    def mod_directory(self) -> str | None:
        try:
            with req.urlopen(f"{self.base_url}/moddirectory", timeout=1) as response:
                return response.read().decode('utf-8').replace('"', "")
        except URLError:
            return None
