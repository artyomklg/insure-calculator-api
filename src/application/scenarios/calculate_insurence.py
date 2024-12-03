from src.application.protocols.tariff import ITariffReader
from src.application.scenarios.contracts.calculate_insurence import (
    CalculateInsuranseRequest,
    CalculateInsuranseResponse,
)
from src.domain.exceptions.tariff import TariffNotFoundError


class CalculateInsuranse:
    def __init__(self, tariff_reader: ITariffReader) -> None:
        self._tariff_reader = tariff_reader

    async def __call__(self, data: CalculateInsuranseRequest) -> CalculateInsuranseResponse:
        tariff = await self._tariff_reader.get_actual_tariff_by_type(data.cargo_type)
        if tariff is None:
            raise TariffNotFoundError(data.cargo_type)
        insurance = tariff.calculate_insurance(data.declared_value)
        return CalculateInsuranseResponse(insurance)
