import os
import ast
import numpy as np
import pandas as pd


def load_cmu_movies_data(path):
    """
    Load and parse the CMU Movie Summary Corpus datasets from specified directory.

    Reads three key dataset files:
    - plot_summaries.txt: Movie plot summaries
    - movie.metadata.tsv: Movie metadata (revenue, runtime, etc.)
    - character.metadata.tsv: Character and actor information

    Args:
        path (str): Base directory path containing the MovieSummaries folder

    Returns:
        tuple: Contains three pandas DataFrames:
            - df_movies: Movie metadata (wiki_id, name, release_date, etc.)
            - df_plots: Plot summaries for each movie
            - df_characters: Character and actor metadata
    """

    if "MovieSummaries" not in os.listdir(path):
        raise FileNotFoundError(
            "MovieSummaries directory not found in specified path. Please first download the dataset from http://www.cs.cmu.edu/~ark/personas/ and extract it to the data/MovieSummaries folder."
        )

    # Load Plot Summaries
    plot_summaries_file = f"{path}MovieSummaries/plot_summaries.txt"
    df_plots = pd.read_csv(
        plot_summaries_file,
        sep="\t",
        header=None,
        names=["wiki_movie_id", "plot_summary"],
    )

    # Load Movie Metadata
    movie_metadata_file = f"{path}MovieSummaries/movie.metadata.tsv"
    df_movies = pd.read_csv(movie_metadata_file, sep="\t", header=None)
    df_movies.columns = [
        "wiki_movie_id",
        "freebase_movie_id",
        "movie_name",
        "movie_release_date",
        "movie_box_office_revenue",
        "movie_runtime",
        "movie_languages",
        "movie_countries",
        "movie_genres",
    ]

    # Load Character Metadata
    character_metadata_file = f"{path}MovieSummaries/character.metadata.tsv"
    df_characters = pd.read_csv(character_metadata_file, sep="\t", header=None)
    df_characters.columns = [
        "wiki_movie_id",
        "freebase_movie_id",
        "movie_release_date",
        "character_name",
        "actor_dob",
        "actor_gender",
        "actor_height",
        "actor_ethnicity",
        "actor_name",
        "actor_age_at_release",
        "freebase_character_actor_map_id",
        "freebase_character_id",
        "freebase_actor_id",
    ]

    return df_movies, df_plots, df_characters


def parse_date(date_str):
    """
    Parse a date string into a pandas datetime object.
    """
    try:
        return pd.to_datetime(date_str)
    except:
        return pd.NaT


def parse_dict(field):
    """
    Convert dictionary to a tuple (key, value) pairs
    """
    try:
        return [x for x in ast.literal_eval(field).items()]
    except:
        return []


def preprocess_cmu_movies_data(df_movies, df_characters):
    """
    Clean and standardize CMU movie and character datasets.

    Performs the following operations:
    - Converts numeric fields to appropriate data types
    - Standardizes date fields to datetime format
    - Parses structured fields (languages, countries, genres)

    Args:
        df_movies (pd.DataFrame): Raw movies metadata
        df_characters (pd.DataFrame): Raw character metadata

    Returns:
        tuple: Contains two preprocessed DataFrames:
            - df_movies: Cleaned movie metadata
            - df_characters: Cleaned character metadata
    """
    # Convert appropriate columns to numeric data types
    df_movies["movie_box_office_revenue"] = pd.to_numeric(
        df_movies["movie_box_office_revenue"], errors="coerce"
    )
    df_movies["movie_runtime"] = pd.to_numeric(
        df_movies["movie_runtime"], errors="coerce"
    )

    # Convert release date to datetime
    df_movies["movie_release_date"] = df_movies["movie_release_date"].apply(parse_date)
    df_characters["movie_release_date"] = df_characters["movie_release_date"].apply(
        parse_date
    )
    df_characters["actor_dob"] = df_characters["actor_dob"].apply(parse_date)

    # Process JSON-like fields
    df_movies["movie_languages"] = df_movies["movie_languages"].apply(parse_dict)
    df_movies["movie_countries"] = df_movies["movie_countries"].apply(parse_dict)
    df_movies["movie_genres"] = df_movies["movie_genres"].apply(parse_dict)

    return df_movies, df_characters


def load_tmdb_data(path):
    """
    Load TMDB movies metadata from CSV file.

    Args:
        path (str): Base directory path containing the TMDB folder

    Returns:
        pd.DataFrame: Raw TMDB movies metadata
    """

    if "TMDB" not in os.listdir(path):
        raise FileNotFoundError(
            "TMDB directory not found in specified path. Please first download the dataset from https://www.kaggle.com/rounakbanik/the-movies-dataset and extract it to the data/TMDB folder."
        )

    tmdb_metadata_file = f"{path}TMDB/movies_metadata.csv"
    df_tmdb = pd.read_csv(tmdb_metadata_file, low_memory=False)
    return df_tmdb


def preprocess_tmdb_data(df_tmdb):
    """
    Clean and standardize TMDB dataset.

    Performs the following operations:
    - Extracts date components (year, month, day)
    - Converts financial fields to numeric format
    - Replaces zero values with NaN in budget/revenue

    Args:
        df_tmdb (pd.DataFrame): Raw TMDB metadata

    Returns:
        pd.DataFrame: Preprocessed TMDB metadata with standardized fields
    """
    # Extract release year, month, and day from release_date
    df_tmdb["release_date"] = pd.to_datetime(df_tmdb["release_date"], errors="coerce")
    df_tmdb["release_year"] = df_tmdb["release_date"].dt.year
    df_tmdb["release_month"] = df_tmdb["release_date"].dt.month
    df_tmdb["release_day"] = df_tmdb["release_date"].dt.day

    # Convert budget and revenue to numeric, coerce errors to NaN
    df_tmdb["budget"] = pd.to_numeric(df_tmdb["budget"], errors="coerce")
    df_tmdb["revenue"] = pd.to_numeric(df_tmdb["revenue"], errors="coerce")

    # Replace zero values with NaN
    df_tmdb["budget"].replace(0, np.nan, inplace=True)
    df_tmdb["revenue"].replace(0, np.nan, inplace=True)

    return df_tmdb


def load_imdb_data(path):
    """
    Load core IMDb datasets from compressed TSV files.

    Loads four key IMDb datasets:
    - title.basics: Basic movie information
    - title.ratings: User ratings data
    - title.crew: Director and writer credits
    - name.basics: Personal information for crew/cast

    Args:
        path (str): Base directory path containing the IMDB folder

    Returns:
        tuple: Contains four DataFrames:
            - df_title_basics: Basic title information
            - df_title_ratings: Rating statistics
            - df_title_crew: Crew information
            - df_name_basics: Personal/biographical data
    """

    if "IMDB" not in os.listdir(path):
        raise FileNotFoundError(
            "IMDB directory not found in specified path. Please first download the dataset from https://datasets.imdbws.com and extract it to the data/IMDB folder."
        )

    title_basics_file = f"{path}IMDB/title.basics.tsv.gz"
    title_ratings_file = f"{path}IMDB/title.ratings.tsv.gz"
    title_crew_file = f"{path}IMDB/title.crew.tsv.gz"
    name_basics_file = f"{path}IMDB/name.basics.tsv.gz"

    df_title_basics = pd.read_csv(title_basics_file, sep="\t", low_memory=False)
    df_title_ratings = pd.read_csv(title_ratings_file, sep="\t", low_memory=False)
    df_title_crew = pd.read_csv(title_crew_file, sep="\t", low_memory=False)
    df_name_basics = pd.read_csv(name_basics_file, sep="\t", low_memory=False)

    return df_title_basics, df_title_ratings, df_title_crew, df_name_basics


def preprocess_imdb_data(
    df_title_basics, df_title_ratings, df_title_crew, df_name_basics
):
    """
    Prepare IMDb datasets for merging and analysis.

    Currently serves as a placeholder for future preprocessing steps.

    Args:
        df_title_basics (pd.DataFrame): Basic title information
        df_title_ratings (pd.DataFrame): Rating statistics
        df_title_crew (pd.DataFrame): Crew information
        df_name_basics (pd.DataFrame): Personal/biographical data

    Returns:
        tuple: Contains four preprocessed DataFrames in the same order
    """
    # Placeholder for any preprocessing steps if needed later on
    return df_title_basics, df_title_ratings, df_title_crew, df_name_basics
