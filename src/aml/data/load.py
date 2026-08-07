from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PATH = PROJECT_ROOT / "data" / "processed"

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

def load_raw_data(file_name: str = "raw", path: str | Path = PATH, dtypes=DTYPES) -> pd.DataFrame:
    """
    Just loads dataset .parquet without feature engineering and splits
    """
    input_path = Path(path)
    if not input_path.exists():
            raise FileNotFoundError(f"Specified directory does not exist: {input_path}")
    df = pd.read_parquet(path / f"{file_name}.parquet")

    df = (
    df.drop_duplicates()
      .sort_values("Timestamp", kind="mergesort")
      .reset_index(drop=True)
    )

    return df

def load_dataset_splits(input_dir: str | Path = PATH, 
                        target_col: str = "Is Laundering",
                        sets: list = None,
                        ) -> dict[str, tuple[pd.DataFrame, pd.Series]]:
    """
    Loads splits of the dataset from Parquet files, separated by X and Y.
    
    input_dir: path to the folder containing the files.
    target_col: target ("Is Laundering")
    sets: None - if you need to load all splits
        ["..."] - if you only need a few of them (["train", "val"])
    """

    input_path = Path(input_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Specified directory does not exist: {input_path}")

    splits = {}

    if not sets:
        for file_path in input_path.glob('*.parquet'):
            split_name = file_path.stem
            df = pd.read_parquet(file_path)

            actual_target = (
                target_col
                if target_col in df.columns
                else ("target" if "target" in df.columns else df.columns[-1])
                )
            X = df.drop(columns=[actual_target])
            y = df[actual_target]
            splits[split_name] = (X, y)
    else:
        for split_name in sets:
            if ".parquet" in split_name:
                file_path = input_path / split_name
            else:
                file_path = input_path / f"{split_name}.parquet"

            df = pd.read_parquet(file_path)
            actual_target = (
                target_col
                if target_col in df.columns
                else ("target" if "target" in df.columns else df.columns[-1])
                )
            X = df.drop(columns=[actual_target])
            y = df[actual_target]
            splits[split_name] = (X, y)

    if not splits:
        raise FileNotFoundError(
            f"В директории {input_path} не найдено .parquet файлов."
        )
    
    return splits