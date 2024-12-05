import datetime
from dataclasses import asdict
from typing import Sequence

from sqlalchemy import delete, func, insert, select

from src.domain.entities.tariff import Tariff
from src.domain.protocols.tariff import ITariff
from src.infrastructure.persistence.models.tariff import TariffORM
from src.infrastructure.persistence.repositories.sqla_session_mixin import SqlalchemySessionMixin


class SqlalchemyTariffRepository(SqlalchemySessionMixin):
    async def get_actual_tariff_by_type(self, cargo_type: str) -> ITariff | None:
        res = await self._session.execute(
            select(TariffORM)
            .filter(
                TariffORM.cargo_type == cargo_type,
                TariffORM.date <= datetime.datetime.now(datetime.UTC).date(),
            )
            .order_by(TariffORM.date.desc())
        )
        tariff = res.scalar_one_or_none()
        if not tariff:
            return None
        return Tariff(
            tariff_id=tariff.tariff_id,
            cargo_type=tariff.cargo_type,
            rate=tariff.rate,
            date=tariff.date,
        )

    async def get_available_cargo_types(self) -> Sequence[str]:
        res = await self._session.execute(select(TariffORM.cargo_type.distinct()))
        return res.scalars().all()

    async def get_all_tariffs(self) -> list[Tariff]:
        res = await self._session.execute(select(TariffORM))
        return [
            Tariff(
                tariff_id=tariff.tariff_id,
                cargo_type=tariff.cargo_type,
                rate=tariff.rate,
                date=tariff.date,
            )
            for tariff in res.scalars().all()
        ]

    async def get_tariffs_by_date(self, date: datetime.date) -> list[Tariff]:
        res = await self._session.execute(select(TariffORM).filter(TariffORM.date == date))
        return [
            Tariff(
                tariff_id=tariff.tariff_id,
                cargo_type=tariff.cargo_type,
                rate=tariff.rate,
                date=tariff.date,
            )
            for tariff in res.scalars().all()
        ]

    async def get_tariffs_count(self) -> int:
        res = await self._session.execute(select(func.count()).select_from(TariffORM))
        return res.scalar_one()

    async def get_tariffs_count_by_date(self, date: datetime.date) -> int:
        res = await self._session.execute(
            select(func.count()).select_from(TariffORM).filter(TariffORM.date == date)
        )
        return res.scalar_one()

    async def add_tariffs(self, tariffs: Sequence[Tariff]) -> None:
        await self._session.execute(insert(TariffORM), [asdict(tariff) for tariff in tariffs])

    async def delete_by_date(self, date: datetime.date) -> None:
        await self._session.execute(delete(TariffORM).filter(TariffORM.date == date))

    async def delete_all_tariffs(self) -> None:
        await self._session.execute(delete(TariffORM))
