import datetime
from collections import defaultdict
from typing import Sequence

from src.application.dto.log_message import LogMessageDTO
from src.application.protocols.log import ILogMessageSaver
from src.application.protocols.tariff import ITariffReader, ITariffSaver
from src.application.protocols.transaction_context import ITransactionContext
from src.application.scenarios.contracts.tariff import TariffItem, TariffRequest
from src.domain.entities.tariff import Tariff
from src.domain.exceptions.tariff import (
    AppendTariffsWhenStorageByDateNotEmptyError,
    UploadTariffsWhenStorageNotEmptyError,
)


class TariffService:
    def __init__(
        self,
        tariff_reader: ITariffReader,
        tariff_saver: ITariffSaver,
        tc: ITransactionContext,
        log_saver: ILogMessageSaver,
    ) -> None:
        self._tariff_reader = tariff_reader
        self._tariff_saver = tariff_saver
        self._log_saver = log_saver
        self._tc = tc

    async def get_available_cargo_types(self) -> list[str]:
        return await self._tariff_reader.get_available_cargo_types()

    async def get_all(self) -> dict[datetime.date, list[TariffItem]]:
        tariffs = await self._tariff_reader.get_all_tariffs()
        response: dict[datetime.date, list[TariffItem]] = defaultdict(list)

        for tariff in tariffs:
            response[tariff.date].append(
                TariffItem(
                    cargo_type=tariff.cargo_type,
                    rate=tariff.rate,
                )
            )
        return dict(response)

    async def get_by_date(self, date: datetime.date) -> list[TariffItem]:
        tariffs = await self._tariff_reader.get_tariffs_by_date(date)
        return [TariffItem(cargo_type=tariff.cargo_type, rate=tariff.rate) for tariff in tariffs]

    async def upload(self, data: Sequence[TariffRequest]) -> None:
        await self._upload(data)
        await self._log_saver.log(LogMessageDTO.new_append())
        await self._tc.commit()

    async def append_by_date(self, data: TariffRequest) -> None:
        await self._append_by_date(data)
        await self._log_saver.log(LogMessageDTO.new_append())
        await self._tc.commit()

    async def change(self, data: Sequence[TariffRequest]) -> None:
        await self._delete_all()
        await self._upload(data)
        await self._log_saver.log(LogMessageDTO.new_edit())
        await self._tc.commit()

    async def change_by_date(self, data: TariffRequest) -> None:
        await self._delete_by_date(data.date)
        await self._append_by_date(data)
        await self._log_saver.log(LogMessageDTO.new_edit())
        await self._tc.commit()

    async def delete_all(self) -> None:
        await self._delete_all()
        await self._log_saver.log(LogMessageDTO.new_delete())
        await self._tc.commit()

    async def delete_by_date(self, delete_date: datetime.date) -> None:
        await self._delete_by_date(delete_date)
        await self._log_saver.log(LogMessageDTO.new_delete())
        await self._tc.commit()

    async def _upload(self, data: Sequence[TariffRequest]) -> None:
        tariffs_count = await self._tariff_reader.get_tariffs_count()
        if tariffs_count > 0:
            raise UploadTariffsWhenStorageNotEmptyError()
        tariffs: list[Tariff] = []
        for tariff in data:
            tariffs.extend(
                [
                    Tariff.create(
                        cargo_type=tariff_item.cargo_type, rate=tariff_item.rate, date=tariff.date
                    )
                    for tariff_item in tariff.items
                ]
            )
        Tariff.validate_upload_tariffs(tariffs)
        await self._tariff_saver.add_tariffs(tariffs)

    async def _append_by_date(self, data: TariffRequest) -> None:
        tariffs_count = await self._tariff_reader.get_tariffs_count_by_date(data.date)
        if tariffs_count > 0:
            raise AppendTariffsWhenStorageByDateNotEmptyError(data.date)
        tariffs: list[Tariff] = [
            Tariff.create(cargo_type=tariff_item.cargo_type, rate=tariff_item.rate, date=data.date)
            for tariff_item in data.items
        ]
        Tariff.validate_upload_tariffs(tariffs)
        await self._tariff_saver.add_tariffs(tariffs)

    async def _delete_all(self) -> None:
        await self._tariff_saver.delete_all_tariffs()

    async def _delete_by_date(self, delete_date: datetime.date) -> None:
        await self._tariff_saver.delete_by_date(delete_date)
