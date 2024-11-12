import pandas as pd
import numpy as np


def merge_cmu_tmdb_data(df_movies, df_tmdb):
    """
    Merges CMU movies data with TMDB data.

    Args:
        df_movies (pd.DataFrame): CMU movies dataframe.
        df_tmdb (pd.DataFrame): TMDB movies dataframe.

    Returns:
        df_movies_merged (pd.DataFrame): Merged dataframe.
    """
    # Ensure movie_release_date is in datetime format and extract year, month, and day
    df_movies["movie_release_date"] = pd.to_datetime(
        df_movies["movie_release_date"], errors="coerce"
    )
    df_movies["release_year"] = df_movies["movie_release_date"].dt.year
    df_movies["release_month"] = df_movies["movie_release_date"].dt.month
    df_movies["release_day"] = df_movies["movie_release_date"].dt.day

    # Merge the TMDB dataset with the existing df_movies DataFrame
    df_movies_merged = pd.merge(
        df_movies,
        df_tmdb[
            [
                "title",
                "release_year",
                "release_month",
                "release_day",
                "revenue",
                "budget",
                "imdb_id",
            ]
        ],
        left_on=["movie_name", "release_year"],
        right_on=["title", "release_year"],
        how="left",
    )

    # Create a combined revenue column
    df_movies_merged["combined_revenue"] = df_movies_merged["revenue"].combine_first(
        df_movies_merged["movie_box_office_revenue"]
    )

    # Create combined release_month and release_day columns
    df_movies_merged["release_month"] = df_movies_merged[
        "release_month_x"
    ].combine_first(df_movies_merged["release_month_y"])
    df_movies_merged["release_day"] = df_movies_merged["release_day_x"].combine_first(
        df_movies_merged["release_day_y"]
    )

    # Drop the redundant columns
    df_movies_merged.drop(
        columns=[
            "release_month_x",
            "release_month_y",
            "release_day_x",
            "release_day_y",
            "title",
        ],
        inplace=True,
    )

    return df_movies_merged


def merge_with_imdb_data(
    df_movies_merged, df_title_basics, df_title_ratings, df_title_crew, df_name_basics
):
    """
    Merges the merged CMU and TMDB data with IMDb data.

    Args:
        df_movies_merged (pd.DataFrame): Dataframe after merging CMU and TMDB data.
        df_title_basics (pd.DataFrame): IMDb title basics dataframe.
        df_title_ratings (pd.DataFrame): IMDb title ratings dataframe.
        df_title_crew (pd.DataFrame): IMDb title crew dataframe.
        df_name_basics (pd.DataFrame): IMDb name basics dataframe.

    Returns:
        df_movies_combined (pd.DataFrame): Dataframe after merging with IMDb data.
    """
    # Merge with IMDb title_basics
    df_movies_combined = pd.merge(
        df_movies_merged,
        df_title_basics[["tconst", "primaryTitle", "startYear"]],
        left_on="imdb_id",
        right_on="tconst",
        how="left",
    )

    # Merge with IMDb title_ratings
    df_movies_combined = pd.merge(
        df_movies_combined,
        df_title_ratings[["tconst", "averageRating", "numVotes"]],
        left_on="imdb_id",
        right_on="tconst",
        how="left",
    )

    # Merge with IMDb title_crew
    df_movies_combined = pd.merge(
        df_movies_combined,
        df_title_crew[["tconst", "directors"]],
        left_on="imdb_id",
        right_on="tconst",
        how="left",
    )

    # Get the first mentioned director
    df_movies_combined["first_director"] = (
        df_movies_combined["directors"].str.split(",").str[0]
    )

    # Merge with name.basics to get director details
    df_movies_combined = pd.merge(
        df_movies_combined,
        df_name_basics[["nconst", "primaryName"]],
        left_on="first_director",
        right_on="nconst",
        how="left",
    )

    # Rename the column to 'director'
    df_movies_combined.rename(columns={"primaryName": "director"}, inplace=True)

    # Drop the redundant columns
    df_movies_combined.drop(
        columns=[
            "tconst_x",
            "tconst_y",
            "tconst",
            "directors",
            "first_director",
            "nconst",
        ],
        inplace=True,
    )

    return df_movies_combined
