import datetime
import uuid

from sqlalchemy import types as sa_types
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base import BaseORM


class TariffORM(BaseORM):
    __tablename__ = "tariffs"

    tariff_id: Mapped[uuid.UUID] = mapped_column(sa_types.UUID(as_uuid=True), primary_key=True)
    cargo_type: Mapped[str]
    rate: Mapped[float]
    date: Mapped[datetime.date] = mapped_column(index=True)
