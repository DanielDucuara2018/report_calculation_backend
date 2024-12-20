"""Added Telegram and Exchanges model + user_name, password and email in User model

Revision ID: 3f6496c5961a
Revises: cbb52317e246
Create Date: 2024-03-06 20:50:49.363095

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "3f6496c5961a"
down_revision = "cbb52317e246"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "exchange",
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("update_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("creation_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("exchange_name", sa.String(), nullable=False, server_default=""),
        sa.Column("api_key", sa.String(), nullable=False, server_default=""),
        sa.Column("secret_key", sa.String(), nullable=False, server_default=""),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.user_id"],
        ),
        sa.PrimaryKeyConstraint("exchange_name"),
    )
    op.create_table(
        "telegram",
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("update_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("creation_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("telegram_id", sa.String(), nullable=False, server_default=""),
        sa.Column("token", sa.String(), nullable=False, server_default=""),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.user_id"],
        ),
        sa.PrimaryKeyConstraint("telegram_id"),
    )
    op.add_column(
        "user", sa.Column("user_name", sa.String(), nullable=False, server_default="")
    )
    op.add_column(
        "user",
        sa.Column("password", sa.LargeBinary(), nullable=False, server_default=""),
    )
    op.add_column(
        "user", sa.Column("email", sa.String(), nullable=True, server_default="")
    )


def downgrade():
    op.drop_column("user", "email")
    op.drop_column("user", "password")
    op.drop_column("user", "user_name")
    op.drop_table("telegram")
    op.drop_table("exchange")
