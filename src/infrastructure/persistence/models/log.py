import datetime
import uuid
from typing import Literal

from sqlalchemy import types as sa_types
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base import BaseORM


class LogMessageORM(BaseORM):
    __tablename__ = "log_messages"

    log_id: Mapped[uuid.UUID] = mapped_column(sa_types.UUID, primary_key=True)
    user_id: Mapped[str | None] = mapped_column(sa_types.String(36))
    action: Mapped[Literal["append", "edit", "delete"]] = mapped_column(sa_types.String(10))
    logged_at: Mapped[datetime.datetime]
    is_sended: Mapped[bool] = mapped_column(server_default="false")
