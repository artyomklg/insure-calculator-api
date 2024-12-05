import datetime
from typing import Protocol, Sequence

from src.domain.entities.tariff import Tariff
from src.domain.protocols.tariff import ITariff


class ITariffReader(Protocol):
    async def get_actual_tariff_by_type(self, cargo_type: str) -> ITariff | None:
        """Взять актуальный (самый новый по дате) тариф по его типу, либо ничего."""

    async def get_available_cargo_types(self) -> list[str]:
        """Взять доступные типы грузов."""

    async def get_all_tariffs(self) -> list[Tariff]:
        """Взять все тарифы. Отсортировано по уменьшению даты."""

    async def get_tariffs_by_date(self, date: datetime.date) -> list[Tariff]:
        """Взять тарифы за конкретную дату."""

    async def get_tariffs_count(self) -> int:
        """Узнать кол-во тарифов"""

    async def get_tariffs_count_by_date(self, date: datetime.date) -> int:
        """Узнать кол-во тарифов за конкретную дату."""


class ITariffSaver(Protocol):
    async def add_tariffs(self, tariffs: Sequence[Tariff]) -> None:
        """Добавление тарифов, если таких нет"""

    async def delete_by_date(self, date: datetime.date) -> None:
        """Удаление тарифов по дате."""

    async def delete_all_tariffs(self) -> None:
        """Удаление всех тарифов."""
