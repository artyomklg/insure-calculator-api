import datetime
from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body

from src.application.scenarios.calculate_insurence import CalculateInsuranse
from src.application.scenarios.contracts.calculate_insurence import (
    CalculateInsuranseRequest,
    CalculateInsuranseResponse,
)
from src.application.scenarios.contracts.tariff import TariffItem, TariffRequest
from src.application.scenarios.tariff_service import TariffService
from src.presentation.webapi.examples import REQUEST_EXAMPLE, RESPONSE_EXAMPLE
from src.presentation.webapi.schemas.requests import TariffDTO

router = APIRouter(prefix="/tariff", route_class=DishkaRoute, tags=["Тарифы"])


@router.post("/calculate", tags=["Расчёт стоимости страхования"])
async def calculate_insurance(
    request_data: CalculateInsuranseRequest, action: Annotated[CalculateInsuranse, FromComponent()]
) -> CalculateInsuranseResponse:
    return await action(request_data)


@router.get("", responses=RESPONSE_EXAMPLE)
async def get_all_tariffs(
    service: Annotated[TariffService, FromComponent()],
) -> dict[datetime.date, list[TariffItem]]:
    """Получения всех имеющихся тарифов"""
    return await service.get_all()


@router.get(
    "/{date}",
)
async def get_tariff_by_date(
    date: datetime.date, service: Annotated[TariffService, FromComponent()]
) -> list[TariffItem]:
    """Получения всех имеющихся тарифов"""
    return await service.get_by_date(date)


@router.post("")
async def upload_tariffs(
    request_data: Annotated[
        dict[datetime.date, list[TariffDTO]], Body(embed=False, example=REQUEST_EXAMPLE)
    ],
    service: Annotated[TariffService, FromComponent()],
) -> None:
    """
    Загрузка тарифов в путое хранилище.
    При попытке загрузить данные не в пустое хранилище выдает ошибку.
    """
    return await service.upload(
        data=[
            TariffRequest(
                date=date,
                items=[
                    TariffItem(cargo_type=tariff.cargo_type, rate=tariff.rate) for tariff in tariffs
                ],
            )
            for date, tariffs in request_data.items()
        ]
    )


@router.post("/{date}")
async def append_tariff_by_date(
    date: datetime.date,
    request_data: Annotated[list[TariffDTO], Body(embed=False)],
    service: Annotated[TariffService, FromComponent()],
) -> None:
    """Добавление тарифа на конкретную дату."""
    return await service.append_by_date(
        data=TariffRequest(
            date=date,
            items=[
                TariffItem(cargo_type=tariff.cargo_type, rate=tariff.rate)
                for tariff in request_data
            ],
        )
    )


@router.put("")
async def change_tariffs(
    request_data: Annotated[
        dict[datetime.date, list[TariffDTO]], Body(embed=False, example=REQUEST_EXAMPLE)
    ],
    service: Annotated[TariffService, FromComponent()],
) -> None:
    """Изменение всех тарифов."""
    return await service.change(
        data=[
            TariffRequest(
                date=date,
                items=[
                    TariffItem(cargo_type=tariff.cargo_type, rate=tariff.rate) for tariff in tariffs
                ],
            )
            for date, tariffs in request_data.items()
        ]
    )


@router.patch("/{date}")
async def change_tariff_by_date(
    date: datetime.date,
    request_data: Annotated[list[TariffDTO], Body(embed=False)],
    service: Annotated[TariffService, FromComponent()],
) -> None:
    """Обновление тарифа на конкретную дату."""
    return await service.change_by_date(
        data=TariffRequest(
            date=date,
            items=[
                TariffItem(cargo_type=tariff.cargo_type, rate=tariff.rate)
                for tariff in request_data
            ],
        )
    )


@router.delete("")
async def delete_all_tariffs(service: Annotated[TariffService, FromComponent()]) -> None:
    """Очищает все тарифы в хранилище."""
    return await service.delete_all()


@router.delete("/{date}")
async def delete_tariff_by_date(
    date: datetime.date, service: Annotated[TariffService, FromComponent()]
) -> None:
    """Очищает тарифы на конкретную дату."""
    return await service.delete_by_date(date)
