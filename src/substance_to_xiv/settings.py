import json
import os
from typing import Any


class Settings:
    def __init__(self, path: str = "settings.json"):
        self.path = path
        self._data = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except json.JSONDecodeError:
                self._data = {}
        else:
            self._save()

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._save()

    def delete(self, key: str) -> None:
        if key in self._data:
            del self._data[key]
            self._save()

    def all(self) -> dict:
        return dict(self._data)


# settings = Settings()

# # Set values
# settings.set("volume", 60)
# settings.set("theme", "dark")
# settings.set("debug", True)

# # Get values
# volume = settings.get("volume", 50)
# theme = settings.get("theme")

# missing_setting = settings.get("theme2")
# print(missing_setting)

# # Remove a setting
# settings.delete("debug")

# # Get all settings
# print(settings.all())
