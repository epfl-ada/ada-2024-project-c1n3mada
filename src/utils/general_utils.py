def perform_final_checks(df):
    """
    Perform final validation checks on the processed dataset.

    Parameters:
    -----------
    df : pandas.DataFrame
        The final processed DataFrame

    Returns:
    --------
    bool
        True if all checks pass, False otherwise
    """
    checks_passed = True

    print("Performing final data quality checks...")

    # Check 1: No negative revenues
    neg_revenues = df[df["inflated_revenue"] < 0]
    if not neg_revenues.empty:
        print(
            f"WARNING: Found {len(neg_revenues)} movies with negative inflated revenues"
        )
        checks_passed = False

    # Check 2: No future release dates
    future_movies = df[df["release_year"] > 2024]
    if not future_movies.empty:
        print(
            f"WARNING: Found {len(future_movies)} movies with release dates in the future"
        )
        checks_passed = False

    # Check 3: Verify essential columns exist
    essential_columns = [
        "movie_name",
        "release_year",
        "combined_revenue",
        "inflated_revenue",
        "movie_genres",
        "averageRating",
    ]
    missing_columns = [col for col in essential_columns if col not in df.columns]
    if missing_columns:
        print(f"WARNING: Missing essential columns: {missing_columns}")
        checks_passed = False

    # Check 4: Verify data completeness
    null_counts = df[essential_columns].isnull().sum()
    if null_counts.any():
        print("\nNull values in essential columns:")
        print(null_counts[null_counts > 0])
        checks_passed = False

    # Check 5: Verify revenue inflation worked correctly
    inflation_ratio = df["inflated_revenue"].mean() / df["combined_revenue"].mean()
    if not (0.5 < inflation_ratio < 10):  # reasonable range for inflation multiplier
        print(f"WARNING: Unusual inflation ratio: {inflation_ratio:.2f}")
        checks_passed = False

    # Summary statistics
    if checks_passed:
        print("\nAll checks passed! Dataset summary:")
        print(f"Total number of movies: {len(df):,}")
        print(
            f"Date range: {df['release_year'].min():.0f} to {df['release_year'].max():.0f}"
        )
        print(
            f"Average inflation-adjusted revenue: ${df['inflated_revenue'].mean():,.2f}"
        )
        print(
            f"Number of unique genres: {len(set([genre for genres in df['movie_genres'] for genre in genres]))}"
        )

    return checks_passed


def adjust_for_inflation(df, cpi, target_year=2016):
    """
    Adjust revenues for inflation using CPI data.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing movie data with 'combined_revenue' and 'release_year' columns
    cpi : pandas.DataFrame
        DataFrame containing CPI data
    target_year : int, optional (default=2016)
        The year to adjust all values to

    Returns:
    --------
    pandas.DataFrame
        DataFrame with new 'inflated_revenue' column
    """
    # Verify target year is in CPI data
    if target_year not in cpi["year"].values:
        raise ValueError(f"Target year {target_year} not found in CPI data")

    # Get CPI value for target year
    target_year_cpi = cpi[cpi["year"] == target_year]["CPIAUCNS"].values[0]

    # Calculate inflation-adjusted revenue
    df = df.copy()
    df["inflated_revenue"] = df.apply(
        lambda x: x["combined_revenue"]
        * target_year_cpi
        / cpi[cpi["year"] == x["release_year"]]["CPIAUCNS"].values[0],
        axis=1,
    )

    # calculate inflation-adjusted budget
    df["inflated_budget"] = df.apply(
        lambda x: x["budget"]
        * target_year_cpi
        / cpi[cpi["year"] == x["release_year"]]["CPIAUCNS"].values[0],
        axis=1,
    )

    return df
