import datetime
from dataclasses import dataclass


@dataclass
class TariffItem:
    cargo_type: str
    rate: float


@dataclass
class TariffRequest:
    date: datetime.date
    items: list[TariffItem]
