from dataclasses import dataclass, field
from typing import Any


@dataclass
class TemplateContext:
    _data: dict[str, Any] = field(default_factory=dict)

    def get(self, path: str) -> any:
        parts = path.split('.')
        current = self._data
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
                if current is None:
                    raise KeyError(f"Путь '{path}' не найден")
            else:
                current = getattr(current, part, None)
                if current is None:
                    raise KeyError(f"Путь '{path}' не найден")

        return current

    def set(self, key: str, value: any) -> None:
        self._data[key] = value

    def copy(self):
        return TemplateContext(self._data.copy())
