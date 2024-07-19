"""Change user tablename to account

Revision ID: e4eae37c05e4
Revises: 882689bacaf1
Create Date: 2024-07-19 15:50:46.990225

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "e4eae37c05e4"
down_revision = "882689bacaf1"
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table("user", "account")


def downgrade():
    op.rename_table("account", "user")
