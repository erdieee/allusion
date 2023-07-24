import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def flatten_dicts(nested_list: List[Any]) -> List[Dict[str, Any]]:
    result = []
    for item in nested_list:
        if isinstance(item, dict):
            result.append(item)
        elif isinstance(item, list):
            result.extend(flatten_dicts(item))
    return result


def store_dict_to_json(data: Dict[str, Any], file_name: str) -> None:
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)


def load_json_to_dict(file_name: str) -> Dict[str, Any]:
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data


def parse_date(date_string: str, date_format: Optional[str] = None) -> str:
    if not date_format:
        date_format = "%A,%d %b %Y,%H:%M"
    date_string = date_string.replace("  ", " ")
    datetime_obj = datetime.strptime(date_string, date_format).isoformat()
    return datetime_obj


def _df_best_odds(df: pd.DataFrame) -> pd.DataFrame:
    odds_columns = [col for col in df.columns if "odds" in col]
    tmp = df.drop(odds_columns, axis=1).drop("book", axis=1).head(1)
    for col in odds_columns:
        max_row_idx = df[col].idxmax()
        max_value = df.at[max_row_idx, col]
        max_book = df.at[max_row_idx, "book"]
        book_col = str(col).replace("odds", "book")
        tmp[col] = max_value
        tmp[book_col] = max_book

    return tmp


def get_df_best_odds(df: pd.DataFrame) -> pd.DataFrame:
    new_df = pd.DataFrame()
    leagues = df["league"].unique()
    for league in leagues:
        lgs = df[df["league"] == league]
        matches = lgs["match"].unique()
        for match in matches:
            tmp = lgs[lgs["match"] == match]
            tmp = _df_best_odds(tmp)
            if new_df.empty:
                new_df = tmp
            else:
                new_df = pd.concat([new_df, tmp])
    new_df = new_df.reset_index(drop=True)
    return new_df


def check_arbitrage(df: pd.DataFrame) -> pd.DataFrame:
    odds_columns = [col for col in df.columns if "odds" in col]
    reciprocal_df = 1 / df[odds_columns]
    df["reciprocal_sum"] = reciprocal_df.sum(axis=1)
    df["arbitrage"] = df["reciprocal_sum"] < 1
    df = df[df["arbitrage"] == True]
    return df
