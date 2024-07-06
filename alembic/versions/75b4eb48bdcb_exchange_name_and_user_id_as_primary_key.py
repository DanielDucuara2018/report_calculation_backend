"""exchange_name and user_id as primary key

Revision ID: 75b4eb48bdcb
Revises: 3f6496c5961a
Create Date: 2024-03-08 10:44:03.777746

"""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

from alembic import op

# revision identifiers, used by Alembic.
revision = "75b4eb48bdcb"
down_revision = "3f6496c5961a"
branch_labels = None
depends_on = None

enum_exchange_name = ENUM("BINANCE", "OKX", name="enum_exchange_name")


def upgrade():
    enum_exchange_name.create(op.get_bind())
    op.alter_column("exchange", "user_id", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_column("exchange", "exchange_name")
    op.add_column(
        "exchange",
        sa.Column(
            "exchange_name",
            type_=enum_exchange_name,
            server_default="BINANCE",
            nullable=False,
        ),
    )
    op.create_primary_key("exchange_pkey", "exchange", ["user_id", "exchange_name"])
    op.drop_constraint("exchange_user_id_fkey", "exchange", type_="foreignkey")
    op.create_foreign_key(
        "exchange_user_id_fkey",
        "exchange",
        "user",
        ["user_id"],
        ["user_id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("exchange_user_id_fkey", "exchange", type_="foreignkey")
    op.create_foreign_key(
        "exchange_user_id_fkey", "exchange", "user", ["user_id"], ["user_id"]
    )
    op.drop_column("exchange", "exchange_name")
    op.add_column(
        "exchange", sa.Column("exchange_name", sa.String(), server_default="BINANCE")
    )
    op.create_primary_key("exchange_pkey", "exchange", ["exchange_name"])
    op.alter_column("exchange", "user_id", existing_type=sa.VARCHAR(), nullable=True)
    enum_exchange_name.drop(op.get_bind())
