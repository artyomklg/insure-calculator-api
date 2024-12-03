"""initial

Revision ID: b0351a7207ba
Revises:
Create Date: 2024-12-03 23:06:14.684766

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b0351a7207ba"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "log_messages",
        sa.Column("log_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=True),
        sa.Column("action", sa.String(length=10), nullable=False),
        sa.Column("logged_at", sa.DateTime(), nullable=False),
        sa.Column("is_sended", sa.Boolean(), server_default="false", nullable=False),
        sa.PrimaryKeyConstraint("log_id", name=op.f("pk_log_messages")),
    )
    op.create_table(
        "tariffs",
        sa.Column("tariff_id", sa.UUID(), nullable=False),
        sa.Column("cargo_type", sa.String(), nullable=False),
        sa.Column("rate", sa.Float(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("tariff_id", name=op.f("pk_tariffs")),
    )
    op.create_index(op.f("ix_tariffs_date"), "tariffs", ["date"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tariffs_date"), table_name="tariffs")
    op.drop_table("tariffs")
    op.drop_table("log_messages")
