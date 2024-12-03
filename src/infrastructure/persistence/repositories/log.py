import uuid
from dataclasses import asdict
from typing import Sequence

from sqlalchemy import insert, select, update

from src.application.dto.log_message import LogMessageDTO
from src.infrastructure.persistence.models.log import LogMessageORM
from src.infrastructure.persistence.repositories.sqla_session_mixin import SqlalchemySessionMixin


class SqlalchemyLogMessageRepository(SqlalchemySessionMixin):
    async def get_all_logs(self, limit: int) -> Sequence[LogMessageDTO]:
        res = await self._session.execute(
            select(LogMessageORM)
            .filter(LogMessageORM.is_sended.is_(False))
            .limit(limit)
            .with_for_update()
        )
        return [
            LogMessageDTO(
                log_id=log.log_id,
                user_id=log.user_id,
                action=log.action,
                logged_at=log.logged_at,
            )
            for log in res.scalars().all()
        ]

    async def log(self, message: LogMessageDTO) -> None:
        await self._session.execute(insert(LogMessageORM).values(**asdict(message)))

    async def mark_as_sended_by_ids(self, ids: Sequence[uuid.UUID]) -> None:
        await self._session.execute(
            update(LogMessageORM).filter(LogMessageORM.log_id.in_(ids)).values(is_sended=True)
        )
