from typing import Protocol, runtime_checkable


@runtime_checkable
class ITransactionContext(Protocol):
    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
