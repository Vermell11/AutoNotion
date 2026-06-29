"""Cálculo determinista de duración para cierres de sesión."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SessionDuration:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start.tzinfo is None or self.end.tzinfo is None:
            raise ValueError("Inicio y fin deben incluir zona horaria.")
        if self.end < self.start:
            raise ValueError("El fin no puede ser anterior al inicio.")

    @classmethod
    def from_iso(cls, start: str, end: str) -> "SessionDuration":
        return cls(datetime.fromisoformat(start), datetime.fromisoformat(end))

    @property
    def seconds(self) -> int:
        return round((self.end - self.start).total_seconds())

    @property
    def minutes(self) -> float:
        return round(self.seconds / 60, 2)

    @property
    def hours(self) -> float:
        return round(self.seconds / 3600, 2)
