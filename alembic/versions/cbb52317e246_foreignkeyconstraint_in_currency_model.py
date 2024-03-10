"""ForeignKeyConstraint in currency model

Revision ID: cbb52317e246
Revises: 96f48aad0810
Create Date: 2023-08-07 16:02:25.540553

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "cbb52317e246"
down_revision = "96f48aad0810"
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        None,
        "currency_pair",
        "user",
        ["user_id"],
        ["user_id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint(None, "currency_pair", type_="foreignkey")
