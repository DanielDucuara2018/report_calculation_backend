"""Add user_id as primary key for purchase model

Revision ID: 1bac194306cc
Revises: 841bca3f6dd1
Create Date: 2024-03-18 10:42:59.725098

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "1bac194306cc"
down_revision = "841bca3f6dd1"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("purchase", "user_id", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_constraint("purchase_pkey", "purchase", type_="primary")
    op.create_primary_key("purchase_pkey", "purchase", ["user_id", "purchase_id"])


def downgrade():
    op.drop_constraint("purchase_pkey", "purchase", type_="primary")
    op.create_primary_key("purchase_pkey", "purchase", ["purchase_id"])
    op.alter_column("purchase", "user_id", existing_type=sa.VARCHAR(), nullable=True)
