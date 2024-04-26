"""Remove Telegram_id from User model

Revision ID: 17461526ba96
Revises: 1bac194306cc
Create Date: 2024-03-22 16:11:31.294568

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "17461526ba96"
down_revision = "1bac194306cc"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("user", "telegram_id")


def downgrade():
    op.add_column(
        "user",
        sa.Column(
            "telegram_id",
            sa.VARCHAR(),
            default=None,
            autoincrement=False,
            nullable=True,
        ),
    )
