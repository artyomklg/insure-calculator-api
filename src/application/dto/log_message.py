import datetime
import uuid
from dataclasses import dataclass
from typing import Any, Literal


@dataclass(kw_only=True)
class LogMessageDTO:
    log_id: uuid.UUID
    user_id: Any | None
    action: Literal["append", "edit", "delete"]
    logged_at: datetime.datetime

    @classmethod
    def new_append(cls: type["LogMessageDTO"], user_id: Any | None = None) -> "LogMessageDTO":
        return cls(
            log_id=uuid.uuid4(),
            user_id=user_id,
            action="append",
            logged_at=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
        )

    @classmethod
    def new_edit(cls: type["LogMessageDTO"], user_id: Any | None = None) -> "LogMessageDTO":
        return cls(
            log_id=uuid.uuid4(),
            user_id=user_id,
            action="edit",
            logged_at=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
        )

    @classmethod
    def new_delete(cls: type["LogMessageDTO"], user_id: Any | None = None) -> "LogMessageDTO":
        return cls(
            log_id=uuid.uuid4(),
            user_id=user_id,
            action="delete",
            logged_at=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
        )
