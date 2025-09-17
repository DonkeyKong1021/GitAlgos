"""add refresh token table"""
from alembic import op
import sqlalchemy as sa

revision = "20240115000000"
down_revision = "20240101000000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("token", sa.String(length=512), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.create_index("ix_refresh_user", "refresh_tokens", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_refresh_user", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
