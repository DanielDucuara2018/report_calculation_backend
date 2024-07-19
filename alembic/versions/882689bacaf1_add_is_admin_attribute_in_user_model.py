"""Add is_admin attribute in user model

Revision ID: 882689bacaf1
Revises: 17461526ba96
Create Date: 2024-07-19 15:23:49.915177

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "882689bacaf1"
down_revision = "17461526ba96"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade():
    op.drop_column("user", "is_admin")
