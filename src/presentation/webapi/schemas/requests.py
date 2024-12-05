from pydantic import BaseModel


class TariffDTO(BaseModel):
    cargo_type: str
    rate: float


class CalculateInsuranseQuery(BaseModel):
    declared_value: float
    cargo_type: str
