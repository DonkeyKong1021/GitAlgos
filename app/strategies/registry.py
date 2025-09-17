from pathlib import Path
from typing import Dict

EXAMPLES_DIR = Path(__file__).resolve().parent / "examples"


def list_example_strategies() -> Dict[str, str]:
    result: Dict[str, str] = {}
    for path in EXAMPLES_DIR.glob("*.py"):
        result[path.stem] = path.read_text()
    return result
