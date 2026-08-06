from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PATH = PROJECT_ROOT / "data" / "processed" / "raw.parquet"

TARGET = "Is Laundering"
CSV_COLUMNS = [
    "Timestamp",
    "From Bank",
    "Account",
    "To Bank",
    "Account.1",
    "Amount Received",
    "Receiving Currency",
    "Amount Paid",
    "Payment Currency",
    "Payment Format",
    TARGET,
]
DTYPES = {
    "From Bank": "string",
    "Account": "string",
    "To Bank": "string",
    "Account.1": "string",
    "Amount Received": "float64",
    "Receiving Currency": "string",
    "Amount Paid": "float64",
    "Payment Currency": "string",
    "Payment Format": "string",
    TARGET: "int8",
}

def load_data(path: str | Path = PATH, dtypes=DTYPES) -> pd.DataFrame:
    df = pd.read_parquet(path)

    df['hour'] = df["Timestamp"].dt.hour
    df['dayofweek'] = df["Timestamp"].dt.dayofweek
    df['day'] = df["Timestamp"].dt.day
    df['month'] = df["Timestamp"].dt.month

    df = (
    df.drop_duplicates()
      .sort_values("Timestamp", kind="mergesort")
      .reset_index(drop=True)
    )

    return df
