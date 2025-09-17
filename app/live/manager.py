from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class RiskLimits:
    daily_loss_limit: float
    max_position: float


class LiveTradingManager:
    def __init__(self) -> None:
        self.active_sessions: Dict[str, Dict] = {}

    def start(self, user_id: int, broker: str, strategy_id: int, risk_limits: RiskLimits) -> Dict:
        session = {
            "user_id": user_id,
            "broker": broker,
            "strategy_id": strategy_id,
            "risk_limits": risk_limits.__dict__,
            "started_at": datetime.utcnow().isoformat(),
            "pnl": 0.0,
        }
        self.active_sessions[str(user_id)] = session
        return session

    def stop(self, user_id: int) -> None:
        self.active_sessions.pop(str(user_id), None)

    def status(self, user_id: int) -> Optional[Dict]:
        return self.active_sessions.get(str(user_id))

    def killswitch(self, user_id: int) -> Dict:
        self.stop(user_id)
        return {"status": "stopped"}


_manager = LiveTradingManager()


def get_manager() -> LiveTradingManager:
    return _manager
