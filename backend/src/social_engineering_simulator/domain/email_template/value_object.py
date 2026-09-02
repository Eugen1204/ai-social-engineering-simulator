from dataclasses import dataclass, field
from typing import Any

from social_engineering_simulator.domain.email_template.services.exceptions import TemplateTextTooLongError, \
    EmptyTemplateTextError


@dataclass
class TemplateContext:
    _data: dict[str, Any] = field(default_factory=dict)

    def get(self, path: str) -> Any:
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


@dataclass(frozen=True)
class SubjectText:
    value: str

    def __post_init__(self):
        if not self.value.split():
            raise EmptyTemplateTextError("value cannot be empty")
        if len(self.value) > 200:
            raise TemplateTextTooLongError("Value is too long, max=200")


@dataclass(frozen=True)
class ContentText:
    value: str

    def __post_init__(self):
        if not self.value.split():
            raise EmptyTemplateTextError("value cannot be empty")
        if len(self.value) > 5000:
            raise TemplateTextTooLongError("Value is too long, max=5000")


@dataclass
class RenderedTemplate:
    subject: str
    content: str
