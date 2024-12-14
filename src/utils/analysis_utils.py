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


def extract_first_country(country_list):
    parsed_country_list = ast.literal_eval(country_list)
    return parsed_country_list[0][1] if len(parsed_country_list) > 0 else None
