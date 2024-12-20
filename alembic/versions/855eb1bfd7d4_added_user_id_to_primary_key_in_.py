"""Added user_id to primary key in telegram model

Revision ID: 855eb1bfd7d4
Revises: 75b4eb48bdcb
Create Date: 2024-03-08 14:14:29.984281

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "855eb1bfd7d4"
down_revision = "75b4eb48bdcb"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("telegram", "user_id", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_constraint("telegram_pkey", "telegram", type_="primary")
    op.create_primary_key("telegram_pkey", "telegram", ["user_id", "telegram_id"])
    op.drop_constraint("telegram_user_id_fkey", "telegram", type_="foreignkey")
    op.create_foreign_key(
        "telegram_user_id_fkey",
        "telegram",
        "user",
        ["user_id"],
        ["user_id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("telegram_user_id_fkey", "telegram", type_="foreignkey")
    op.create_foreign_key(
        "telegram_user_id_fkey", "telegram", "user", ["user_id"], ["user_id"]
    )
    op.drop_constraint("telegram_pkey", "telegram", type_="primary")
    op.create_primary_key("telegram_pkey", "telegram", ["telegram_id"])
    op.alter_column("telegram", "user_id", existing_type=sa.VARCHAR(), nullable=True)
