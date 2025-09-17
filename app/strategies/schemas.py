from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None
    assets: List[str]
    timeframe: str
    params: Dict[str, Any] = Field(default_factory=dict)
    code: str


class StrategyCreate(StrategyBase):
    pass


class StrategyUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    assets: Optional[List[str]]
    timeframe: Optional[str]
    params: Optional[Dict[str, Any]]
    code: Optional[str]


class StrategyRead(StrategyBase):
    id: int

    class Config:
        orm_mode = True
