import datetime
import uuid
from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence

from src.domain.exceptions.tariff import UploadTariffsRepeatTypesInDateError


@dataclass
class Tariff:
    tariff_id: uuid.UUID
    cargo_type: str
    rate: float
    date: datetime.date

    def calculate_insurance(self, declared_value: float) -> float:
        return declared_value * self.rate

    @classmethod
    def create(
        cls: type["Tariff"],
        *,
        cargo_type: str,
        rate: float,
        date: datetime.date,
    ) -> "Tariff":
        return cls(
            tariff_id=uuid.uuid4(),
            cargo_type=cargo_type,
            rate=rate,
            date=date,
        )

    @staticmethod
    def validate_upload_tariffs(tariffs: Sequence["Tariff"]) -> None:
        tarif_types_by_date_groups: dict[datetime.date, list[str]] = defaultdict(list)
        for tariff in tariffs:
            tarif_types_by_date_groups[tariff.date].append(tariff.cargo_type)
        error_dates: list[datetime.date] = []
        for date, types in tarif_types_by_date_groups.items():
            if len(types) != len(set(types)):
                error_dates.append(date)
        if error_dates:
            raise UploadTariffsRepeatTypesInDateError(error_dates)
