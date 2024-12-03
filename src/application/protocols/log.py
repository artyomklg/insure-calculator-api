import uuid
from typing import Protocol, Sequence

from src.application.dto.log_message import LogMessageDTO


class ILogMessageReader(Protocol):
    async def get_all_logs(self) -> Sequence[LogMessageDTO]:
        """Возвращает все логи"""


class ILogMessageSaver(Protocol):
    async def log(self, message: LogMessageDTO) -> None:
        """Новый лог"""

    async def mark_as_sended_by_ids(self, ids: Sequence[uuid.UUID]) -> None:
        """Удаляет логи по id"""
