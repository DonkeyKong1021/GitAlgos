import builtins
import math
from types import MappingProxyType
from typing import Any, Dict

import numpy as np
import pandas as pd

ALLOWED_BUILTINS = {"abs", "min", "max", "range", "len", "enumerate", "zip", "float", "int", "sum"}


class SandboxExecutionError(Exception):
    pass


class StrategySandbox:
    def __init__(self) -> None:
        self._globals: Dict[str, Any] = {
            "np": np,
            "pd": pd,
            "math": math,
        }

    def execute(self, code: str, context: Dict[str, Any]) -> Dict[str, Any]:
        safe_builtins = {name: getattr(builtins, name) for name in ALLOWED_BUILTINS}
        sandbox_globals = {
            "__builtins__": MappingProxyType(safe_builtins),
            **self._globals,
            **context,
        }
        sandbox_locals: Dict[str, Any] = {}
        try:
            exec(code, sandbox_globals, sandbox_locals)
        except Exception as exc:  # noqa: BLE001
            raise SandboxExecutionError(str(exc)) from exc
        sandbox_globals.update(sandbox_locals)
        return sandbox_globals


def run_strategy(code: str, context: Dict[str, Any]) -> Dict[str, Any]:
    sandbox = StrategySandbox()
    return sandbox.execute(code, context)
