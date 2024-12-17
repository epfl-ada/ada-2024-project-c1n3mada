import ast
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr, f_oneway


def genre_correlation(df, genre):
    genre_data = df[df["genres_list"].apply(lambda x: genre in x)]
    pearson_corr, _ = pearsonr(
        genre_data["averageRating"], np.log10(genre_data["inflated_revenue"])
    )
    spearman_corr, _ = spearmanr(
        genre_data["averageRating"], np.log10(genre_data["inflated_revenue"])
    )
    return pd.Series(
        {"Genre": genre, "Pearson": pearson_corr, "Spearman": spearman_corr}
    )


def extract_names(columns):
    names = []
    for column in columns:
        literals = ast.literal_eval(column)
        names.extend([literals[1] for literals in literals])
    return names


def extract_first_language(language_list):
    parsed_language_list = ast.literal_eval(language_list)
    return parsed_language_list[0][1] if len(parsed_language_list) > 0 else None


def extract_languages(language_list):
    """
    Extract the language names from a list of tuples
    Args:
        language_list (str): a string representation of a list of tuples (each tuple contains a language code and language name)
    Returns:
        list: a list containing only the language names
    """
    parsed_language_list = ast.literal_eval(language_list)
    return [
        item[1]
        for item in parsed_language_list
        if isinstance(item, tuple) and len(item) > 1
    ]


def extract_first_country(country_list):
    parsed_country_list = ast.literal_eval(country_list)
    return parsed_country_list[0][1] if len(parsed_country_list) > 0 else None


def get_movies_with_genres(df, genres):
    """
    Get a list of movies that have at least one of the specified genres.

    Args:
        df (pd.DataFrame): DataFrame containing movie data
        genres (list): List of genres to search for

    Returns:
        list: List of movie names
    """
    set_genres = set(genres)
    movies = []
    for movie_name, genre_list in zip(df["movie_name"], df["genres_list"]):
        # make the genre_list a set
        set_movie_genres = set(genre_list)
        # check if the intersection is not empty
        if set_movie_genres.intersection(set_genres):
            movies.append(movie_name)
    return movies


def calculate_count_revenue_correlation(mean_revenue_pivot, genre_year_pivot):
    correlation_results = []
    genres = genre_year_pivot.columns
    for genre in genres:
        # create a combined dataframe
        combined_df = pd.DataFrame(
            {
                "mean_revenue": mean_revenue_pivot[genre],
                "movie_count": genre_year_pivot[genre],
            }
        )

        # drop rows where mean revenue or count is 0
        filtered_df = combined_df[
            (combined_df["mean_revenue"] > 0) & (combined_df["movie_count"] > 0)
        ]

        if not filtered_df.empty:
            # calculate Pearson and Spearman correlations
            pearson_corr, _ = pearsonr(
                filtered_df["mean_revenue"], filtered_df["movie_count"]
            )
            spearman_corr, _ = spearmanr(
                filtered_df["mean_revenue"], filtered_df["movie_count"]
            )

            # append results to the list
            correlation_results.append(
                {"Genre": genre, "Pearson": pearson_corr, "Spearman": spearman_corr}
            )

    # convert the list to a dataframe
    correlation_df = pd.DataFrame(correlation_results)
    correlation_df = correlation_df.set_index("Genre").sort_index()
    return correlation_df
