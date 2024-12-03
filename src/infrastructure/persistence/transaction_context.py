from dataclasses import dataclass
from types import TracebackType
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SqlalchemyTransactionContext:
    _session: AsyncSession

    async def __aenter__(self) -> "SqlalchemyTransactionContext":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> None:
        if exc_value:
            await self.rollback()
        else:
            await self._close_transaction()

    async def commit(self) -> None:
        await self._session.commit()
        await self._close_transaction()

    async def rollback(self) -> None:
        await self._session.rollback()
        await self._close_transaction()

    async def _close_transaction(self) -> None:
        await self._session.close()


async def transaction_context_factory(
    session: AsyncSession,
) -> AsyncGenerator[SqlalchemyTransactionContext, None]:
    async with SqlalchemyTransactionContext(session) as tc:
        yield tc
