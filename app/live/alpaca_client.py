from typing import Dict, List


class AlpacaClient:
    def __init__(self, key_id: str, secret: str, paper: bool = True) -> None:
        self.key_id = key_id
        self.secret = secret
        self.paper = paper

    def submit_order(self, symbol: str, qty: float, side: str, order_type: str = "market", limit_price: float | None = None) -> Dict:
        return {"symbol": symbol, "qty": qty, "side": side, "type": order_type, "status": "filled"}

    def get_positions(self) -> List[Dict]:
        return []

    def get_account(self) -> Dict:
        return {"equity": 100000, "cash": 100000}
