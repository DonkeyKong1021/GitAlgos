from typing import Dict, List


class OandaClient:
    def __init__(self, token: str, account: str, practice: bool = True) -> None:
        self.token = token
        self.account = account
        self.practice = practice

    def submit_order(self, instrument: str, units: float, side: str, order_type: str = "market", price: float | None = None) -> Dict:
        return {"instrument": instrument, "units": units, "side": side, "type": order_type, "status": "filled"}

    def get_positions(self) -> List[Dict]:
        return []

    def get_account(self) -> Dict:
        return {"balance": 100000, "unrealizedPL": 0}
