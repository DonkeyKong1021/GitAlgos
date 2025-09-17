"""initial schema"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20240101000000"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="user"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "strategies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("params", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("assets", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("timeframe", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    op.create_table(
        "backtest_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("strategy_id", sa.Integer(), sa.ForeignKey("strategies.id"), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("settings", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("metrics", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("equity_path", sa.String(length=512), nullable=True),
        sa.Column("report_path", sa.String(length=512), nullable=True),
    )

    op.create_table(
        "api_credentials",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("broker", sa.String(length=50), nullable=False),
        sa.Column("key_id", sa.String(length=255), nullable=False),
        sa.Column("secret_encrypted", sa.LargeBinary(), nullable=False),
        sa.Column("paper", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "backtest_trades",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("backtest_id", sa.Integer(), sa.ForeignKey("backtest_runs.id"), nullable=False),
        sa.Column("dt", sa.DateTime(timezone=True), nullable=False),
        sa.Column("symbol", sa.String(length=50), nullable=False),
        sa.Column("side", sa.String(length=10), nullable=False),
        sa.Column("qty", sa.Float(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("fee", sa.Float(), nullable=True),
    )

    op.create_table(
        "backtest_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("backtest_id", sa.Integer(), sa.ForeignKey("backtest_runs.id"), nullable=False),
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
    )

    op.create_index("ix_strategies_owner", "strategies", ["owner_id"])
    op.create_index("ix_backtest_owner", "backtest_runs", ["owner_id"])
    op.create_index("ix_trades_backtest", "backtest_trades", ["backtest_id"])


def downgrade() -> None:
    op.drop_index("ix_trades_backtest", table_name="backtest_trades")
    op.drop_index("ix_backtest_owner", table_name="backtest_runs")
    op.drop_index("ix_strategies_owner", table_name="strategies")
    op.drop_table("backtest_metrics")
    op.drop_table("backtest_trades")
    op.drop_table("api_credentials")
    op.drop_table("backtest_runs")
    op.drop_table("strategies")
    op.drop_table("users")
