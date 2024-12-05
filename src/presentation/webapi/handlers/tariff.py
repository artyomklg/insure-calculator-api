import datetime
from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Query

from src.application.scenarios.calculate_insurence import CalculateInsuranse
from src.application.scenarios.contracts.calculate_insurence import (
    CalculateInsuranseRequest,
    CalculateInsuranseResponse,
)
from src.application.scenarios.contracts.tariff import TariffItem, TariffRequest
from src.application.scenarios.tariff_service import TariffService
from src.presentation.webapi.examples import REQUEST_EXAMPLE, RESPONSE_EXAMPLE
from src.presentation.webapi.schemas.requests import CalculateInsuranseQuery, TariffDTO

router = APIRouter()


router_calculate = APIRouter(
    prefix="/tariff", route_class=DishkaRoute, tags=["Расчёт стоимости страхования"]
)


@router_calculate.get("/calculate")
async def calculate_insurance(
    request_data: Annotated[CalculateInsuranseQuery, Query()],
    action: Annotated[CalculateInsuranse, FromComponent()],
) -> CalculateInsuranseResponse:
    """Рассчёт стоимости страхования."""
    return await action(
        CalculateInsuranseRequest(
            declared_value=request_data.declared_value,
            cargo_type=request_data.cargo_type,
        )
    )


router_tariffs = APIRouter(prefix="/tariff", route_class=DishkaRoute, tags=["Тарифы"])


@router_tariffs.get("/cargo_types")
async def get_available_cargo_types(
    service: Annotated[TariffService, FromComponent()],
) -> list[str]:
    """Получение доступных типов груза."""
    return await service.get_available_cargo_types()


@router_tariffs.get("", responses=RESPONSE_EXAMPLE)
async def get_all_tariffs(
    service: Annotated[TariffService, FromComponent()],
) -> dict[datetime.date, list[TariffItem]]:
    """Получения всех имеющихся тарифов"""
    return await service.get_all()


@router_tariffs.get("/{date}")
async def get_tariff_by_date(
    date: datetime.date, service: Annotated[TariffService, FromComponent()]
) -> list[TariffItem]:
    """Получения всех имеющихся тарифов"""
    return await service.get_by_date(date)


@router_tariffs.post("")
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


@router_tariffs.post("/{date}")
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


@router_tariffs.put("")
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


@router_tariffs.patch("/{date}")
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


@router_tariffs.delete("")
async def delete_all_tariffs(service: Annotated[TariffService, FromComponent()]) -> None:
    """Очищает все тарифы в хранилище."""
    return await service.delete_all()


@router_tariffs.delete("/{date}")
async def delete_tariff_by_date(
    date: datetime.date, service: Annotated[TariffService, FromComponent()]
) -> None:
    """Очищает тарифы на конкретную дату."""
    return await service.delete_by_date(date)


router.include_router(router_calculate)
router.include_router(router_tariffs)
