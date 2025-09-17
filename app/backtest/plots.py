from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd


def save_equity_curve(equity_curve: pd.Series, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    equity_curve.plot(ax=ax)
    ax.set_title("Equity Curve")
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path
