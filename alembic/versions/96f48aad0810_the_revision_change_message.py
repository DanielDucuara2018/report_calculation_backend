"""The revision change message

Revision ID: 96f48aad0810
Revises: 37b054e87675
Create Date: 2023-08-07 15:24:36.189770

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "96f48aad0810"
down_revision = "37b054e87675"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("user", "telegram_id", existing_type=sa.VARCHAR(), nullable=True)


def downgrade():
    op.alter_column("user", "telegram_id", existing_type=sa.VARCHAR(), nullable=False)
