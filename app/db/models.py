import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default=UserRole.user.value)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    strategies = relationship("Strategy", back_populates="owner", cascade="all, delete-orphan")


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    code = Column(Text, nullable=False)
    params = Column(JSON, nullable=False, default=dict)
    assets = Column(JSON, nullable=False, default=list)
    timeframe = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="strategies")
    backtests = relationship("BacktestRun", back_populates="strategy")


class BacktestStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class BacktestRun(Base):
    __tablename__ = "backtest_runs"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=True)
    status = Column(String(50), nullable=False, default=BacktestStatus.pending.value)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    settings = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    equity_path = Column(String(512), nullable=True)
    report_path = Column(String(512), nullable=True)

    strategy = relationship("Strategy", back_populates="backtests")
    trades = relationship("Trade", back_populates="backtest", cascade="all, delete-orphan")
    metric_rows = relationship("Metric", back_populates="backtest", cascade="all, delete-orphan")


class Trade(Base):
    __tablename__ = "backtest_trades"

    id = Column(Integer, primary_key=True)
    backtest_id = Column(Integer, ForeignKey("backtest_runs.id"), nullable=False)
    dt = Column(DateTime(timezone=True), nullable=False)
    symbol = Column(String(50), nullable=False)
    side = Column(String(10), nullable=False)
    qty = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    fee = Column(Float, nullable=True)

    backtest = relationship("BacktestRun", back_populates="trades")


class Metric(Base):
    __tablename__ = "backtest_metrics"

    id = Column(Integer, primary_key=True)
    backtest_id = Column(Integer, ForeignKey("backtest_runs.id"), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)

    backtest = relationship("BacktestRun", back_populates="metric_rows")


class BrokerType(str, enum.Enum):
    alpaca = "alpaca"
    oanda = "oanda"


class ApiCredential(Base):
    __tablename__ = "api_credentials"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    broker = Column(Enum(BrokerType), nullable=False)
    key_id = Column(String(255), nullable=False)
    secret_encrypted = Column(LargeBinary, nullable=False)
    paper = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    owner = relationship("User")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(512), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)

    user = relationship("User")
