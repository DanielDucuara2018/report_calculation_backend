"""Adding description column

Revision ID: 37b054e87675
Revises:
Create Date: 2023-04-06 15:19:49.983782

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "37b054e87675"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("currency_pair", sa.Column("description", sa.String(), nullable=True))
    op.add_column("purchase", sa.Column("description", sa.String(), nullable=True))
    op.add_column("user", sa.Column("description", sa.String(), nullable=True))


def downgrade():
    op.drop_column("user", "description")
    op.drop_column("purchase", "description")
    op.drop_column("currency_pair", "description")
