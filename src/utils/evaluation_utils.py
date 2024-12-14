import pandas as pd
from typing import Dict


def validate_dataframes(
    df_country: pd.DataFrame,
    df_language: pd.DataFrame,
    df_country_language: pd.DataFrame,
) -> Dict[str, Dict[str, int]]:
    """Validate dataframes for empty lists and duplicates."""

    initial_state = {
        "empty_lists": {
            "countries": count_empty_lists(df_country, "movie_countries"),
            "languages": count_empty_lists(df_language, "movie_languages"),
            "combined": count_empty_lists_combined(df_country_language),
        },
        "duplicates": {
            "countries": df_country.duplicated().sum(),
            "languages": df_language.duplicated().sum(),
            "combined": df_country_language.duplicated().sum(),
        },
    }
    print(f"Empty lists - Countries: {initial_state['empty_lists']['countries']}")
    print(f"Empty lists - Languages: {initial_state['empty_lists']['languages']}")
    print(f"Empty lists - Combined: {initial_state['empty_lists']['combined']}")
    print(f"Duplicates - Countries: {initial_state['duplicates']['countries']}")
    print(f"Duplicates - Languages: {initial_state['duplicates']['languages']}")
    print(f"Duplicates - Combined: {initial_state['duplicates']['combined']}")


def count_empty_lists(df: pd.DataFrame, column: str) -> int:
    return df[df[column] == "[]"].shape[0]


def count_empty_lists_combined(df: pd.DataFrame) -> int:
    return df[(df["movie_countries"] == "[]") | (df["movie_languages"] == "[]")].shape[
        0
    ]
