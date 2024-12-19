import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def plot_genre_barplot(genre_counts, title="Number of Movies per Genre"):
    plt.figure(figsize=(12, 6))
    # use color-blind friendly palette
    sns.barplot(x=genre_counts.index, y=genre_counts.values, palette="Set2")
    plt.title(title)
    plt.xlabel("Genre")
    plt.ylabel("Number of Movies")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


def plot_distribution(
    data,
    column,
    bins=20,
    kde=True,
    color="skyblue",
    title="Distribution",
    xlabel=None,
    ylabel="Frequency",
    transformation=None,
):
    plt.figure(figsize=(10, 6))
    plot_data = transformation(data[column]) if transformation else data[column]
    sns.histplot(plot_data, bins=bins, kde=kde, color=color)
    plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot_scatter(
    df,
    x,
    y,
    title="",
    xlabel=None,
    ylabel=None,
    hue=None,
    alpha=0.7,
    transformation=None,
):
    plt.figure(figsize=(12, 8))
    # use color-blind friendly palette
    plot_y = transformation(df[y]) if transformation else df[y]
    sns.scatterplot(x=x, y=plot_y, data=df, hue=hue, alpha=alpha, palette="Set2")
    plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.show()


def plot_correlation_heatmap(df, cols, title="Correlation Matrix"):
    plt.figure(figsize=(8, 6))
    corr = df[cols].corr()
    # use color-blind friendly palette
    sns.heatmap(corr, annot=True, cmap="crest", fmt=".2f")
    plt.title(title)
    plt.show()


def plot_genre_correlation_bars(
    genre_corrs, title="Correlation between IMDb Ratings and Revenue by Genre"
):
    fig, ax = plt.subplots(figsize=(18, 12))
    genre_corrs_sorted = genre_corrs.sort_values("Pearson", ascending=True)
    x_pearson = genre_corrs_sorted["Pearson"]
    x_spearman = genre_corrs_sorted["Spearman"]
    y = range(len(genre_corrs_sorted.index))

    ax.barh(
        y=[i + 0.2 for i in y],
        width=x_pearson,
        height=0.3,
        color="#2ecc71",
        alpha=0.8,
        label="Pearson",
    )
    ax.barh(
        y=[i - 0.2 for i in y],
        width=x_spearman,
        height=0.3,
        color="#3498db",
        alpha=0.8,
        label="Spearman",
    )

    ax.set_yticks(y)
    ax.set_yticklabels(genre_corrs_sorted.index, fontsize=12)
    ax.set_xlabel("Correlation Coefficient", fontsize=14, fontweight="bold")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    ax.grid(True, axis="x", linestyle="--", alpha=0.7)
    ax.axvline(x=0, color="black", linestyle="-", linewidth=0.5)
    ax.legend(
        title="Correlation Type",
        title_fontsize=12,
        fontsize=12,
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
    )
    for i in y:
        ax.text(
            x_pearson[i],
            i + 0.2,
            f"{x_pearson[i]:.3f}",
            va="center",
            ha="left" if x_pearson[i] >= 0 else "right",
            fontsize=12,
            fontweight="bold",
            color="#16a085",
        )
        ax.text(
            x_spearman[i],
            i - 0.2,
            f"{x_spearman[i]:.3f}",
            va="center",
            ha="left" if x_spearman[i] >= 0 else "right",
            fontsize=12,
            fontweight="bold",
            color="#2980b9",
        )
    plt.tight_layout()
    plt.show()


def create_treemap(data, title, year, mode="movies", top_n=15):
    """
    Create a treemap for a given year.

    Args:
        data: DataFrame containing movie data
        title: Title for the treemap
        year: Year to filter the data
        mode: "movies" for a treemap by top movies, "directors" for a treemap by top directors
        top_n: Number of top entries to include

    Returns:
        Plotly treemap figure
    """
    year_data = data[data["release_year"] == year]  # filter data for the given year

    if mode == "movies":
        col_to_path = ["movie_name"]
        top_data = year_data.nlargest(top_n, "inflated_revenue")[
            ["movie_name", "director", "inflated_revenue"]
        ].reset_index()

    elif mode == "directors":
        col_to_path = ["director"]
        top_data = (
            year_data.groupby("director")["inflated_revenue"]
            .sum()
            .nlargest(top_n)
            .reset_index()
        )  # group by director and sum the revenue
        top_data["movie_name"] = top_data["director"].apply(
            lambda x: year_data[year_data["director"] == x]["movie_name"].tolist()
        )

        top_data["movie_name"] = top_data["movie_name"].apply(
            lambda x: ",".join(x)
        )  # join the movie names to a single string
    else:
        raise ValueError("Invalid mode. Choose 'movies' or 'directors'.")

    # interactive treemap
    fig = px.treemap(
        top_data,
        path=col_to_path,
        values="inflated_revenue",
        color="director",  #
        title=f"Top {top_n} {title} revenue over the years",
        labels={"inflated_revenue": "Revenue"},
        color_discrete_sequence=px.colors.qualitative.Light24,  # .viridis did not have enough colors so we use Light24
        hover_data={
            "movie_name": True,
            "director": True,
            "inflated_revenue": ":.2f",
        },  # Custom hover data
    )
    fig.update_traces(
        hovertemplate="<b>Movie:</b> %{customdata[0]}<br><b>Director:</b> %{customdata[1]}<br><b>Revenue:</b> %{value:$,.0f}",
    )
    # Common layout customization
    fig.update_layout(
        title=dict(font=dict(size=20), x=0.5),
        paper_bgcolor="black",
        font=dict(color="white"),
    )
    return fig


def create_animated_treemap(data, title, mode="movies", top_n=15):
    """
    Create an animated treemap with a slider for each year.

    Args:
        data: DataFrame containing movie data
        mode: "movies" or "directors" for treemap type
        top_n: Number of top entries to include per year

    Returns:
        Plotly figure with animation
    """
    unique_years = sorted(data["release_year"].unique())

    # Create frames for each year
    frames = [
        go.Frame(
            data=create_treemap(data, title, year, mode=mode, top_n=top_n).data,
            name=str(year),
        )
        for year in unique_years
    ]

    # Create initial plot for the first year
    initial_fig = create_treemap(data, title, unique_years[0], mode=mode, top_n=top_n)
    initial_fig.frames = frames

    # Add controls for animation
    initial_fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                        "label": "Pause",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top",
            }
        ],
        sliders=[
            {
                "steps": [
                    {
                        "args": [
                            [str(year)],
                            {
                                "frame": {"duration": 300, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 300},
                            },
                        ],
                        "label": str(year),
                        "method": "animate",
                    }
                    for year in unique_years
                ],
                "active": 0,
                "x": 0.1,
                "len": 0.9,
                "xanchor": "left",
                "y": -0.2,
                "yanchor": "top",
            }
        ],
        width=1200,
        height=600,
    )
    return initial_fig


def plot_budget_revenue_trend(df_budget, min_movies=10):
    # Remove the years with less than 10 movies for more reliable statistics
    df_budget_trend = df_budget.groupby("release_year").filter(
        lambda x: len(x) >= min_movies
    )
    df_budget_trend

    # Calculate annual statistics
    annual_stats = (
        df_budget_trend.groupby("release_year")
        .agg(
            avg_budget=("inflated_budget", "mean"),
            avg_revenue=("inflated_revenue", "mean"),
        )
        .reset_index()
    )

    # Improved plot
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot average budget
    sns.lineplot(
        x="release_year",
        y="avg_budget",
        data=annual_stats,
        ax=ax1,
        linewidth=2.5,
        color="#66C2A5",
        marker="o",
        label="Average Budget",
    )

    # Set labels and formatting
    ax1.set_ylabel("Average Budget", color="#66C2A5")
    ax1.set_xlabel("Release Year")
    ax1.tick_params(axis="y", colors="#66C2A5")
    ax1.yaxis.set_major_formatter(revenue_formatter)

    # Add twin axis for average revenue
    ax2 = ax1.twinx()
    sns.lineplot(
        x="release_year",
        y="avg_revenue",
        data=annual_stats,
        ax=ax2,
        linewidth=2.5,
        color="#FC8D62",
        marker="o",
        label="Average Revenue",
    )

    # Set labels and formatting
    ax2.set_ylabel("Average Revenue", color="#FC8D62")
    ax2.tick_params(axis="y", colors="#FC8D62")
    ax2.yaxis.set_major_formatter(revenue_formatter)

    # Add title and gridlines
    ax1.set_title(
        f"Average Budget and Revenue Over Time ({annual_stats['release_year'].min()} - {annual_stats['release_year'].max()})",
        fontsize=14,
        fontweight="bold",
    )
    ax1.grid(visible=True, linestyle="--", alpha=0.6)

    # Add legends
    ax1.legend(loc="upper left", fontsize=10, frameon=False)
    ax2.legend(loc="upper right", fontsize=10, frameon=False)

    plt.tight_layout()
    plt.show()


def revenue_formatter(x, pos):
    """
    Format revenue to millions or billions with a dollar sign
    """
    if x >= 1e9:
        value = x * 1e-9
        return f"${int(value)}B" if value.is_integer() else f"${value:.1f}B"
    elif x >= 1e6:
        value = x * 1e-6
        return f"${int(value)}M" if value.is_integer() else f"${value:.1f}M"
    return f"${x:.0f}"
