from pydantic import BaseModel


class TariffDTO(BaseModel):
    cargo_type: str
    rate: float
