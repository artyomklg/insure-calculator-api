import datetime
from dataclasses import dataclass

from src.domain.exceptions.base import DomainError


@dataclass
class TariffNotFoundError(DomainError):
    cargo_type: str

    @property
    def message(self) -> str:
        return f"Не найден тарифф для типа {self.cargo_type}"


@dataclass
class UploadTariffsWhenStorageNotEmptyError(DomainError):
    @property
    def message(self) -> str:
        return "Нельзя загрузить тарифы. Они уже существуют."


@dataclass
class AppendTariffsWhenStorageByDateNotEmptyError(DomainError):
    date: datetime.date

    @property
    def message(self) -> str:
        return f"Нельзя загрузить тарифы на {self.date.strftime('%d-%m-%Y')}. Они уже существуют."


@dataclass
class UploadTariffsRepeatTypesInDateError(DomainError):
    error_dates: list[datetime.date]

    @property
    def message(self) -> str:
        str_error_dates = [date.strftime("%d-%m-%Y") for date in self.error_dates]
        return f"В загруженных тарифах присутствует повторение типов в датах: {', '.join(str_error_dates)}."
