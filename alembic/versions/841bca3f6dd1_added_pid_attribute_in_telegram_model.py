"""Added pid attribute in telegram model

Revision ID: 841bca3f6dd1
Revises: 855eb1bfd7d4
Create Date: 2024-03-12 12:53:20.629549

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "841bca3f6dd1"
down_revision = "855eb1bfd7d4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "telegram", sa.Column("pid", sa.Integer(), default=None, nullable=True)
    )


def downgrade():
    op.drop_column("telegram", "pid")
