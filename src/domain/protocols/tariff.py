from typing import Protocol


class ITariff(Protocol):
    def calculate_insurance(self, declared_value: float) -> float: ...
