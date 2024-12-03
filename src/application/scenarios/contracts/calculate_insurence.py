from dataclasses import dataclass


@dataclass
class CalculateInsuranseRequest:
    declared_value: float
    cargo_type: str


@dataclass
class CalculateInsuranseResponse:
    insurance: float
