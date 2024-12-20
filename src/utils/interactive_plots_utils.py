import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import seaborn as sns
import scipy.stats as stats
import statsmodels.api as sm
from scipy.stats import linregress

## ---------- PATHS ---------- #
SAVE_PATH_ECHO = "../c1n3mada-datastory/assets/plots/echo/"
SAVE_PATH_TONGUES = "../c1n3mada-datastory/assets/plots/tongues/"
SAVE_PATH_SHADES = "../c1n3mada-datastory/assets/plots/shades/"
SAVE_PATH_TREASURE = "../c1n3mada-datastory/assets/plots/treasure/"
SAVE_PATH_STARLIGHT = "../c1n3mada-datastory/assets/plots/starlight/"

## ----------INTERACTIVE PLOTS FOR THE MOVIE ECHO ---------- #
def plot_num_of_movies_per_genre(df_rating):
    genre_counts = df_rating.explode("genres_list")["genres_list"].value_counts()
    genre_counts_top20 = genre_counts.head(20).reset_index()
    genre_counts_top20.columns = ["Genre", "Number of Movies"]
    fig = px.bar(
        genre_counts_top20,
        x="Genre",
        y="Number of Movies",
        color="Genre",
        title="Number of Movies per Genre",
        text="Number of Movies",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(
        title=dict(
            text="Number of Movies per Genre",
            font=dict(family="Arial"),
            x=0.5,
        ),
        xaxis=dict(
            title="Genre",
            tickangle=45,
        ),
        yaxis=dict(
            title="Number of Movies",
        ),
        legend_title=dict(text="Genre"),
        template="plotly_white",
        title_x=0.5,
        showlegend=False,
    )
    fig.update_traces(
        texttemplate="%{text}",
        hovertemplate="<b>Genre:</b> %{x}<br><b>Number of Movies:</b> %{y}<extra></extra>",
    )
    fig.write_html(
        f"{SAVE_PATH_ECHO}num_movies_per_genre.html",
        config={"toImageButtonOptions": {"filename": "num_movies_per_genre"}},
    )
    fig.show()


def plot_imdb_rating_distribution(df_rating):
    colors = px.colors.qualitative.Set2
    color = colors[0]
    bins = [i / 2 for i in range(2, 100)]
    counts, bin_edges = np.histogram(df_rating["averageRating"], bins=bins)
    histogram_trace = go.Histogram(
        x=df_rating["averageRating"],
        histnorm="",
        nbinsx=len(bins),
        marker=dict(color=color, line=dict(width=1, color="darkgray")),
        opacity=0.75,
        name="Histogram",
    )
    fig = go.Figure(data=[histogram_trace])
    kde = stats.gaussian_kde(df_rating["averageRating"])
    x_range = np.linspace(
        df_rating["averageRating"].min(), df_rating["averageRating"].max(), 100
    )
    kde_trace = go.Scatter(
        x=x_range,
        y=kde(x_range) * len(df_rating["averageRating"]) / 10,
        mode="lines",
        line=dict(color="#808080", width=2),
        name="KDE",
    )
    fig.add_trace(kde_trace)
    fig.update_layout(
        title_text="IMDb Ratings Distribution",
        title_x=0.5,
        xaxis_title_text="IMDb Rating",
        yaxis_title_text="Number of Movies",
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.01,
        font_color="black",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
        ),
        title_font=dict(family="Arial"),
        template="plotly_white",
        showlegend=False,
    )
    fig.write_html(
        f"{SAVE_PATH_ECHO}imdb_rating_distribution.html",
        config={"toImageButtonOptions": {"filename": "imdb_rating_distribution"}},
    )
    fig.show()


def plot_box_office_revenue_distribution(df_rating):
    log_revenue = np.log10(df_rating["inflated_revenue"])
    colors = px.colors.qualitative.Set2
    color = colors[1]
    histogram_trace = go.Histogram(
        x=log_revenue,
        histnorm="",
        nbinsx=100,
        marker=dict(color=color, line=dict(width=1, color="darkgray")),
        opacity=0.75,
        name="Histogram",
    )
    fig = go.Figure(data=[histogram_trace])
    kde = stats.gaussian_kde(log_revenue)
    x_range = np.linspace(log_revenue.min(), log_revenue.max(), 200)
    kde_trace = go.Scatter(
        x=x_range,
        y=kde(x_range) * len(log_revenue) / 10,
        mode="lines",
        line=dict(color="#808080", width=2),
        name="KDE",
    )
    fig.add_trace(kde_trace)
    fig.update_layout(
        title_text="Box Office Revenue Distribution",
        title_x=0.5,
        xaxis_title_text="Logarithmic Box Office Revenue [$]",
        yaxis_title_text="Number of Movies",
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.01,
        font_color="black",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
        ),
        title_font=dict(family="Arial"),
        showlegend=False,
    )
    fig.write_html(
        f"{SAVE_PATH_ECHO}box_office_revenue_distribution.html",
        config={
            "toImageButtonOptions": {"filename": "box_office_revenue_distribution"}
        },
    )
    fig.show()


def plot_imdb_rating_vs_box_office_revenue(df_rating):
    df_rating["log_revenue"] = np.log10(df_rating["inflated_revenue"])
    fig = px.scatter(
        df_rating,
        x="averageRating",
        y="log_revenue",
        hover_data=["movie_name"],
        title="IMDb Rating vs. Log10 of Box Office Revenue",
        labels={
            "averageRating": "IMDb Rating",
            "log_revenue": "Log10 of Box Office Revenue",
        },
        opacity=0.8,
        color_discrete_sequence=["#0072B2"],
    )
    fig.update_layout(
        xaxis_title="IMDb Rating",
        yaxis_title="Log10 of Box Office Revenue",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="black",
        xaxis=dict(
            showgrid=False, title_font=dict(size=18, color="black")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
            title_font=dict(size=18, color="black"),
        ),
        title=dict(font=dict(size=24, color="black")),
        hovermode="closest",
    )
    fig.update_traces(
        marker=dict(
            size=8, line=dict(width=1, color="darkgray")
        ),
    )
    fig.write_html(
        f"{SAVE_PATH_ECHO}imdb_rating_vs_box_office_revenue.html",
        config={
            "toImageButtonOptions": {"filename": "imdb_rating_vs_box_office_revenue"}
        },
    )
    fig.show()


def plot_correlation_matrix(df_rating):
    custom_labels = {
        "averageRating": "Rating",
        "inflated_revenue": "Revenue",
        "numVotes": "Nbr of Votes",
    }
    renamed_columns = [
        custom_labels[col]
        for col in df_rating[["averageRating", "inflated_revenue", "numVotes"]].columns
    ]
    corr_matrix = df_rating[["averageRating", "inflated_revenue", "numVotes"]].corr()
    corr_matrix.columns = renamed_columns
    corr_matrix.index = renamed_columns
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            text=corr_matrix.values.round(2),
            texttemplate="%{text}",
            hovertemplate="<b>x: %{x}</b><br><b>y: %{y}</b><br><b>Correlation: %{z:.2f}</b>",
            name="Correlation Score",
            colorbar=dict(title="Correlation Score"),
        )
    )
    fig.update_layout(
        title_text="Correlation Between Rating, Revenue and Number of Votes",
        title_x=0.5,
        xaxis=dict(showgrid=False, constrain="domain"),
        yaxis=dict(
            showgrid=False, scaleanchor="x", scaleratio=1
        ),
        coloraxis=dict(colorbar=dict(title="Correlation Score")),
        title_font=dict(family="Arial"),
    )
    fig.write_html(
        f"{SAVE_PATH_ECHO}correlation_matrix.html",
        config={"toImageButtonOptions": {"filename": "correlation_matrix"}},
    )
    fig.show()


def plot_genre_correlation(genre_corrs):
    genre_corrs_sorted = genre_corrs.sort_values("Pearson", ascending=True)
    colors = px.colors.qualitative.Set2
    pearson_color = colors[6]
    spearman_color = colors[7]
    pearson_trace = go.Bar(
        y=genre_corrs_sorted.index,
        x=genre_corrs_sorted["Pearson"],
        orientation="h",
        name="Pearson",
        marker_color=pearson_color,
        hovertemplate="<b>Genre: %{y}</b><br>Pearson Correlation: %{x:.3f}",
    )
    spearman_trace = go.Bar(
        y=genre_corrs_sorted.index,
        x=genre_corrs_sorted["Spearman"],
        orientation="h",
        name="Spearman",
        marker_color=spearman_color,
        hovertemplate="<b>Genre: %{y}</b><br>Spearman Correlation: %{x:.3f}",
    )
    fig = go.Figure(data=[pearson_trace, spearman_trace])
    fig.update_layout(
        title_text="Correlation between IMDb Ratings and Box Office Revenue per Genre",
        xaxis_title="Correlation Coefficient",
        yaxis_title="Genre",
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
            zeroline=True,
            zerolinecolor="gray",
        ),
        yaxis=dict(
            showgrid=False,
            autorange="reversed",
        ),
        legend=dict(title="Correlation Type"),
        barmode="group",
        bargap=0.2,
        bargroupgap=0.1,
        margin=dict(l=0, r=0, t=40, b=0),
        title_font=dict(family="Arial"),
        template="plotly_white",
        title_x=0.5,
    )
    fig.write_html(
        f"{SAVE_PATH_ECHO}genre_correlation.html",
        config={"toImageButtonOptions": {"filename": "genre_correlation"}},
    )
    fig.show()


def plot_3d_regression_plane(df_rating, model_multi):
    averageRating_range = np.linspace(
        df_rating["averageRating"].min(), df_rating["averageRating"].max(), 50
    )
    log_numVotes_range = np.linspace(
        np.log10(df_rating["numVotes"]).min(), np.log10(df_rating["numVotes"]).max(), 50
    )
    averageRating_grid, log_numVotes_grid = np.meshgrid(
        averageRating_range, log_numVotes_range
    )
    predicted_revenue = model_multi.predict(
        sm.add_constant(
            pd.DataFrame(
                {
                    "averageRating": averageRating_grid.ravel(),
                    "log_numVotes": log_numVotes_grid.ravel(),
                }
            )
        )
    ).values.reshape(averageRating_grid.shape)
    actual_x = df_rating["averageRating"]
    actual_y = np.log10(df_rating["numVotes"])
    actual_z = np.log10(df_rating["inflated_revenue"])
    scatter = go.Scatter3d(
        x=actual_x,
        y=actual_y,
        z=actual_z,
        mode="markers",
        marker=dict(
            size=5,
            color=actual_z,
            colorscale="Viridis_r",
            opacity=0.7,
        ),
        name="Actual Data",
        hovertemplate="<b>IMDb Rating:</b> %{x:.2f}<br>"
        "<b>Log10 NumVotes:</b> %{y:.2f}<br>"
        "<b>Log10 Revenue:</b> %{z:.2f}<br>"
        "<b>Movie:</b> %{text}<extra></extra>",
        text=df_rating["movie_name"],
    )
    surface = go.Surface(
        x=averageRating_range,
        y=log_numVotes_range,
        z=predicted_revenue,
        colorscale="Reds",
        opacity=0.7,
        name="Regression Plane",
        showscale=False,
        hoverinfo="skip",
    )
    fig = go.Figure(data=[scatter, surface])
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="IMDb Rating", titlefont=dict(size=12)),
            yaxis=dict(title="Logarithmic Number of Votes", titlefont=dict(size=12)),
            zaxis=dict(title="Logarithmic Revenue [$]", titlefont=dict(size=12)),
        ),
        title=dict(
            text="Regression Model for IMDb Rating, Revenue and Number of Votes",
            x=0.5,
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        template="plotly_white",
        title_font=dict(family="Arial"),
    )
    fig.write_html(
        f"{SAVE_PATH_ECHO}3d_regression_plane.html",
        config={"toImageButtonOptions": {"filename": "3d_regression_plane"}},
    )
    fig.show()


def plot_hexbin_regression_plane(df_rating):
    df_rating["log_revenue"] = np.log10(df_rating["inflated_revenue"])
    x = df_rating["averageRating"]
    y = df_rating["log_revenue"]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    line = slope * x + intercept
    trendline_trace = go.Scatter(
        x=x,
        y=line,
        mode="lines",
        line=dict(color="red", width=2, dash="dash"),
        name=f"(R² = {r_value**2:.3f})",
    )
    hexbin_trace = go.Histogram2d(
        x=df_rating["averageRating"],
        y=df_rating["log_revenue"],
        colorscale="Viridis_r",
        nbinsx=50,
        nbinsy=50,
        showscale=True,
        colorbar=dict(
            title="Number of Movies", len=0.5, y=0.25
        ),
        hovertemplate="IMDb Rating: %{x:.2f}<br>Log Revenue: %{y:.2f}<br>Count: %{z}",
        name="bin",
    )
    x_hist = go.Histogram(
        x=df_rating["averageRating"],
        marker_color="#D3D3D3",
        opacity=0.75,
        marker_line=dict(width=0.07, color="black"),
        yaxis="y2",
        showlegend=False,
        nbinsx=100,
        autobinx=False,
        name="Rating Dist.",
    )
    y_hist = go.Histogram(
        y=df_rating["log_revenue"],
        marker_color="#D3D3D3",
        opacity=0.75,
        marker_line=dict(width=0.07, color="black"),
        xaxis="x2",
        nbinsy=50,
        showlegend=False,
        autobiny=False,
        name="Revenue Dist.",
    )
    layout = go.Layout(
        title_text="Relationship Between IMDb Ratings and Box Office Revenue",
        title_x=0.5,
        title_font=dict(family="Arial"),
        xaxis_title="IMDb Rating",
        yaxis_title="Logarithmic Box Office Revenue [$]",
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            domain=[0, 0.93],
            showgrid=False,
            showticklabels=True,
        ),
        yaxis=dict(
            domain=[0, 0.9],
            showgrid=True,
            gridcolor="lightgray",
            showticklabels=True,
        ),
        xaxis2=dict(
            domain=[0.93, 1], showgrid=False, showticklabels=False
        ),
        yaxis2=dict(
            domain=[0.9, 1], showgrid=False, showticklabels=False
        ),
        margin=dict(t=50, b=0, l=70, r=0),
        legend=dict(
            font=dict(size=12), orientation="h", y=1, x=0.9
        ),
        barmode="overlay",
        bargap=0,
        template="plotly_white",
    )
    fig = go.Figure(data=[hexbin_trace, trendline_trace, x_hist, y_hist], layout=layout)
    fig.write_html(
        f"{SAVE_PATH_ECHO}hexbin_regression_plane.html",
        config={"toImageButtonOptions": {"filename": "hexbin_regression_plane"}},
    )
    fig.show()


## ----------INTERACTIVE PLOTS FOR THE MOVIE SHADES----------#
def create_interactive_number_of_movies_per_genre_plot(genre_counts_top20):
    fig = px.bar(
        x=genre_counts_top20.index,
        y=genre_counts_top20.values,
        title="Number of Movies per Genre",
        labels={"x": "Genre", "y": "Number of Movies"},
        color=genre_counts_top20.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_traces(
        hovertemplate="<b>Genre:</b> %{x}<br><b>Number of Movies:</b> %{y}<extra></extra>"
    )
    fig.update_layout(
        xaxis_tickangle=45,
        xaxis_title="Genre",
        yaxis_title="Number of Movies",
        template="plotly_white",
        bargap=0.2,
        hovermode="closest",
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(pad=dict(t=10, b=0)),
        showlegend=False,
        title_x=0.5,
    )
    os.makedirs("interactive_plots/shades", exist_ok=True)
    fig.write_html(
        f"{SAVE_PATH_SHADES}number_of_movies_per_genre.html",
        config={"toImageButtonOptions": {"filename": "number_of_movies_per_genre"}},
    )
    fig.show()


def create_interactive_number_of_genres_per_movie(num_genres_distribution):
    fig = px.bar(
        x=num_genres_distribution.index,
        y=num_genres_distribution.values,
        title="Number of Genres per Movie Distribution",
        labels={"x": "Number of Genres", "y": "Number of Movies"},
        color=num_genres_distribution.index.astype(str),
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_traces(
        hovertemplate="<b>Number of Genres:</b> %{x}<br><b>Number of Movies:</b> %{y}<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Number of Genres",
        yaxis_title="Number of Movies",
        template="plotly_white",
        bargap=0.2,
        hovermode="closest",
        showlegend=False,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(pad=dict(t=10, b=0)),
        title_x=0.5,
        xaxis=dict(
            title="Number of Genres",
            tickvals=num_genres_distribution.index,
        ),
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}number_of_genres_per_movie.html",
        config={"toImageButtonOptions": {"filename": "number_of_genres_per_movie"}},
    )
    fig.show()


def create_interactive_top_20_genres_with_highest_revenue(mean_genre_revenue):
    top_n = 20
    top_genres = mean_genre_revenue.head(top_n)
    fig = px.bar(
        top_genres,
        x=top_genres.index,
        y="mean",
        title=f"Average Revenue per Genre",
        labels={"x": "Genre", "mean": "Average Box Office Revenue [$]"},
        color=top_genres.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        custom_data="count",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>Genre:</b> %{x}<br>"
            "<b>Average Revenue:</b> $%{y:,.2f}<br>"
            "<b>Number of Movies:</b> %{customdata}"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Average Box Office Revenue [$]",
        xaxis_tickangle=45,
        hovermode="closest",
        template="plotly_white",
        showlegend=False,
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(pad=dict(t=10, b=0)),
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}interactive_top_20_genres_with_highest_revenue.html",
        config={
            "toImageButtonOptions": {"filename": "top_20_genres_with_highest_revenue"}
        },
    )
    fig.show()


def create_interactive_boxplots_revenue_distribution_top_20(
    df_top_genres, mean_genre_order
):
    fig = px.box(
        df_top_genres,
        x="genres_list",
        y="log_revenue",
        title="Box Office Revenue Distribution for Top 20 Genres",
        labels={"genres_list": "Genre", "log_revenue": "Logarithmic Revenue ($)"},
        category_orders={"genres_list": mean_genre_order},
        color="genres_list",
        color_discrete_sequence=px.colors.qualitative.Set2,
        points="outliers",
    )
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Logarithmic Revenue ($)",
        xaxis_tickangle=45,
        template="plotly_white",
        showlegend=False,
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}boxplots_revenue_distribution_top_20.html",
        config={
            "toImageButtonOptions": {"filename": "boxplots_revenue_distribution_top_20"}
        },
    )
    fig.show()


def create_interactive_boxplots_num_genres(df_genres):
    fig = px.box(
        df_genres,
        x="num_genres",
        y="log_revenue",
        title="Box Office Revenue Distribution per Number of Genres",
        labels={
            "num_genres": "Number of Genres",
            "log_revenue": "Logarithmic Revenue ($)",
        },
        color="num_genres",
        color_discrete_sequence=px.colors.qualitative.Set2,
        points="outliers",
    )
    fig.update_layout(
        xaxis_title="Number of Genres",
        yaxis_title="Logarithmic Revenue ($)",
        xaxis_tickangle=0,
        template="plotly_white",
        showlegend=False,
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}boxplots_num_genres.html",
        config={"toImageButtonOptions": {"filename": "boxplots_num_genres"}},
    )
    fig.show()


def create_interactive_avg_revenue_per_num_genres(sorted_avg_revenue):
    sorted_avg_revenue.index = sorted_avg_revenue.index.astype(str)
    fig = px.bar(
        x=sorted_avg_revenue.index,
        y=sorted_avg_revenue.values,
        title="Average Revenue per Number of Genres",
        labels={"x": "Number of Genres", "y": "Average Box Office Revenue ($)"},
        color=sorted_avg_revenue.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        category_orders={"x": sorted_avg_revenue.index.tolist()},
    )
    fig.update_traces(
        hovertemplate=(
            "<b>Number of Genres:</b> %{x}<br>"
            "<b>Average Revenue:</b> $%{y:,.2f}<extra></extra>"
        )
    )
    fig.update_layout(
        xaxis_title="Number of Genres",
        yaxis_title="Average Box Office Revenue ($)",
        template="plotly_white",
        xaxis_tickangle=0,
        bargap=0.2,
        showlegend=False,
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}avg_revenue_per_num_genres.html",
        config={"toImageButtonOptions": {"filename": "avg_revenue_per_num_genres"}},
    )
    fig.show()


def create_interactive_revenue_trends_over_time_heatmap(mean_revenue_pivot):
    mean_revenue_pivot = mean_revenue_pivot.replace(0, np.nan)
    cubehelix_cmap = sns.color_palette("ch:s=-.2,r=.6", as_cmap=True)
    plotly_cubehelix = [
        [i / 255, f"rgb{tuple((np.array(cubehelix_cmap(i / 255)) * 255).astype(int))}"]
        for i in range(256)
    ]
    fig = px.imshow(
        mean_revenue_pivot.T,
        labels=dict(x="Release Year", y="Genre", color="Average Revenue [$]"),
        title="Average Box Office Revenue per Genre Over Time",
        color_continuous_scale=plotly_cubehelix,
        aspect="auto",
    )
    fig.update_layout(
        xaxis=dict(tickangle=45),
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(pad=dict(t=10, b=0)),
        template="plotly_white",
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}revenue_trends_over_time_heatmap.html",
        config={
            "toImageButtonOptions": {"filename": "revenue_trends_over_time_heatmap"}
        },
    )
    fig.show()


def create_interactive_genre_ranking_over_time_racing_barplot(
    mean_revenue_pivot_decade,
):
    mean_revenue_pivot_decade = mean_revenue_pivot_decade.fillna(0)
    genre_colors = px.colors.qualitative.Alphabet
    genre_color_map = {
        genre: genre_colors[i % len(genre_colors)]
        for i, genre in enumerate(mean_revenue_pivot_decade.columns)
    }
    decades = mean_revenue_pivot_decade.index.unique()
    frames = []
    for decade in decades:
        sorted_data = mean_revenue_pivot_decade.loc[decade].sort_values(ascending=False)
        frames.append(
            go.Frame(
                data=[
                    go.Bar(
                        y=sorted_data.index,
                        x=sorted_data.values,
                        orientation="h",
                        marker=dict(
                            color=[
                                genre_color_map[genre] for genre in sorted_data.index
                            ]
                        ),
                        name="Revenue",
                    )
                ],
                name=str(decade),
            )
        )
    initial_decade = decades[0]
    sorted_initial = mean_revenue_pivot_decade.loc[initial_decade].sort_values(
        ascending=False
    )
    layout = go.Layout(
        title="Genre Ranking by Average Box Office Revenue per Decade",
        xaxis=dict(
            title="Average Box Office Revenue [$]",
            range=[0, mean_revenue_pivot_decade.max().max() * 1.1],
        ),
        template="plotly_white",
        title_x=0.5,
        yaxis=dict(autorange="reversed", title="Genres"),
        sliders=[
            {
                "active": 0,
                "steps": [
                    {
                        "label": str(decade),
                        "method": "animate",
                        "args": [
                            [str(decade)],
                            {
                                "frame": {"duration": 2000, "redraw": True},
                                "mode": "immediate",
                            },
                        ],
                    }
                    for decade in decades
                ],
                "x": 0.1,
                "y": -0.1,
                "len": 0.9,
            }
        ],
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 2000, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 100, "easing": "linear"},
                            },
                        ],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
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
                "y": -0.1,
                "yanchor": "top",
            }
        ],
    )
    fig = go.Figure(
        data=[
            go.Bar(
                y=sorted_initial.index,
                x=sorted_initial.values,
                orientation="h",
                marker=dict(
                    color=[genre_color_map[genre] for genre in sorted_initial.index]
                ),
                name="Revenue",
            )
        ],
        layout=layout,
        frames=frames,
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}genre_ranking_over_time_racing_barplot.html",
        config={
            "toImageButtonOptions": {
                "filename": "genre_ranking_over_time_racing_barplot"
            }
        },
    )
    fig.show()


def create_interactive_stacked_area_plot(genre_year_pivot):
    fig = go.Figure()
    for genre in genre_year_pivot.columns:
        fig.add_trace(
            go.Scatter(
                x=genre_year_pivot.index,
                y=genre_year_pivot[genre],
                stackgroup="one",
                name=genre,
                mode="none",
                fill="tonexty",
                hovertemplate=(
                    "<b>Genre:</b> %{fullData.name}<br>"
                    "<b>Release Year:</b> %{x}<br>"
                    "<b>Number of Movies:</b> %{y}<extra></extra>"
                ),
            )
        )
    fig.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Number of Movies",
        template="plotly_white",
        legend_title="Genres",
        xaxis=dict(tickangle=45),
        yaxis=dict(gridcolor="rgba(200,200,200,0.5)"),
        hovermode="x unified",
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(text="Number of Movies per Genre Over Time", pad=dict(t=10, b=0)),
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}stacked_area_plot_genre_over_time.html",
        config={
            "toImageButtonOptions": {"filename": "stacked_area_plot_genre_over_time"}
        },
    )
    fig.show()


def create_interactive_heatmap_genre_over_time(genre_year_pivot):
    cubehelix_cmap = sns.color_palette("ch:s=-.2,r=.6", as_cmap=True)
    plotly_cubehelix = [
        [i / 255, f"rgb{tuple((np.array(cubehelix_cmap(i / 255)) * 255).astype(int))}"]
        for i in range(256)
    ]
    fig = go.Figure(
        data=go.Heatmap(
            z=genre_year_pivot.values,
            x=genre_year_pivot.columns,
            y=genre_year_pivot.index,
            colorscale=plotly_cubehelix,
            colorbar=dict(title="Number of Movies"),
            hovertemplate=(
                "<b>Genre:</b> %{y}<br>"
                "<b>Release Year:</b> %{x}<br>"
                "<b>Number of Movies:</b> %{z}<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Genre",
        xaxis=dict(tickangle=45),
        template="plotly_white",
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(text="Number of Movies per Genre Over Time", pad=dict(t=10, b=0)),
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}heatmap_genre_over_time.html",
        config={"toImageButtonOptions": {"filename": "heatmap_genre_over_time"}},
    )
    fig.show()


def create_interactive_grid(mean_revenue_pivot, genre_year_pivot):
    colors_possible = px.colors.qualitative.Set2
    genres = mean_revenue_pivot.columns.tolist()
    initial_genre = genres[0]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=mean_revenue_pivot.index,
            y=mean_revenue_pivot[initial_genre],
            name="Average Box Office Revenue [$]",
            line=dict(color=colors_possible[3]),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=genre_year_pivot.index,
            y=genre_year_pivot[initial_genre],
            name="Number of Movies",
            line=dict(color=colors_possible[4]),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title=f"Genre: {initial_genre}",
        xaxis_title="Year",
        yaxis_title="Average Box Office Revenue [$]",
        yaxis2_title="Number of Movies",
        yaxis2=dict(showgrid=False),
        template="plotly_white",
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
    )
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=[
                    dict(
                        label=genre,
                        method="update",
                        args=[
                            {
                                "y": [
                                    mean_revenue_pivot[genre],
                                    genre_year_pivot[genre],
                                ]
                            },
                            {"title": f"Genre: {genre}"},
                        ],
                    )
                    for genre in genres
                ],
                x=0,
                y=-0.2,
                xanchor="left",
                yanchor="top",
                direction="up",
            ),
            dict(
                active=2,
                buttons=[
                    dict(
                        label="Revenue",
                        method="update",
                        args=[{"visible": [True, False]}],
                    ),
                    dict(
                        label="Count",
                        method="update",
                        args=[{"visible": [False, True]}],
                    ),
                    dict(
                        label="Both", method="update", args=[{"visible": [True, True]}]
                    ),
                ],
                x=0.3,
                y=-0.2,
                xanchor="left",
                yanchor="top",
                direction="up",
            ),
        ],
    )
    fig.write_html(
        f"{SAVE_PATH_SHADES}grid.html",
        config={"toImageButtonOptions": {"filename": "grid"}},
    )
    fig.show()
    

## ----------INTERACTIVE PLOTS FOR THE MOVIE TONGUES----------#
def top_10_movie_release_countries(top_countries):
    fig = px.bar(
        x=top_countries.values,
        y=top_countries.index,
        title="Top 10 Movie Release Countries",
        labels={"x": "Number of Movies", "y": "Release Country"},
        orientation="h",
        color=top_countries.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        text=top_countries.values,
    )

    fig.update_layout(
        xaxis_title="Number of Movies",
        yaxis_title="Release Country",
        yaxis=dict(categoryorder="total ascending"),
        template="plotly_white",
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(pad=dict(t=10, b=0)),
        showlegend=False,
    )

    fig.show()

    fig.write_html(
        f"{SAVE_PATH_TONGUES}top_10_movie_release_countries.html",
        config={"toImageButtonOptions": {"filename": "top_10_movie_release_countries"}},
    )


def top_10_movie_languages(top_languages):
    fig = px.bar(
        x=top_languages.values,
        y=top_languages.index,
        title="Top 10 Movie Languages",
        labels={"x": "Number of Movies", "y": "Language"},
        orientation="h",
        color=top_languages.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        text=top_languages.values,
    )

    fig.update_layout(
        xaxis_title="Number of Movies",
        yaxis_title="Language",
        yaxis=dict(categoryorder="total ascending"),
        template="plotly_white",
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),  #
        title=dict(pad=dict(t=10, b=0)),
        showlegend=False,
    )

    fig.show()

    fig.write_html(
        f"{SAVE_PATH_TONGUES}top_10_movie_languages.html",
        config={"toImageButtonOptions": {"filename": "top_10_movie_languages"}},
    )


def language_highest_mean_box_office(top_languages, df_movie_country_language_extended):
    df_movie_language_extended_top = df_movie_country_language_extended[
        df_movie_country_language_extended["movie_languages"].isin(top_languages.index)
    ]
    movies_per_language_top = df_movie_language_extended_top.groupby("movie_languages")[
        "movie_name"
    ].nunique()
    movie_counts_aligned = [
        movies_per_language_top.loc[lang] if lang in movies_per_language_top else 0
        for lang in top_languages.index
    ]
    movie_counts_aligned_df = pd.DataFrame(
        movie_counts_aligned, index=top_languages.index
    )
    plot_data_movies = pd.DataFrame(
        {
            "Language": top_languages.index,
            "Average Box Office Revenue [$]": top_languages.values,
            "Movie Count": movie_counts_aligned_df.values.ravel(),
        }
    )

    fig = px.bar(
        data_frame=plot_data_movies,
        x="Language",
        y="Average Box Office Revenue [$]",
        labels={"x": "Language", "y": "Average Box Office Revenue [$]"},
        title=f"Top 10 Languages with Highest Average Box Office Revenue",
        color="Language",
        color_discrete_sequence=px.colors.qualitative.Set2,
        text="Average Box Office Revenue [$]",
        custom_data=["Movie Count"],
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        title_x=0.5,
        title_font=dict(family="Arial"),
        template="plotly_white",
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(pad=dict(t=10, b=0)),
        showlegend=False,
    )

    fig.update_traces(
        texttemplate="%{text:.2s} <br>(%{customdata[0]} movies)",
        textposition="outside",
    )

    fig.update_yaxes(range=[0, max(top_languages.values) * 1.2])

    fig.show()

    fig.write_html(
        f"{SAVE_PATH_TONGUES}language_highest_mean_box_office.html",
        config={
            "toImageButtonOptions": {"filename": "language_highest_mean_box_office"}
        },
    )


def average_revenue_per_language_per_year(filtered_df):
    mean_revenue_pivot_year = filtered_df.pivot(
        index="release_year", columns="movie_languages", values="average_revenue"
    ).fillna(0)
    language_colors = px.colors.qualitative.Set2
    language_color_map = {
        language: language_colors[i % len(language_colors)]
        for i, language in enumerate(mean_revenue_pivot_year.columns)
    }
    all_languages = mean_revenue_pivot_year.columns

    years = mean_revenue_pivot_year.index.unique()
    frames = []
    for year in years:
        sorted_data = mean_revenue_pivot_year.loc[year].sort_values(ascending=False)
        frames.append(
            go.Frame(
                data=[
                    go.Bar(
                        y=all_languages,
                        x=[sorted_data.get(lang, 0) for lang in all_languages],
                        orientation="h",
                        width=0.8,
                        marker=dict(
                            color=[
                                language_color_map[language]
                                for language in all_languages
                            ]
                        ),
                        name="Revenue",
                    )
                ],
                name=str(year),
            )
        )
    initial_year = years[0]
    sorted_initial = (
        mean_revenue_pivot_year.loc[initial_year].reindex(all_languages).fillna(0)
    )

    max_revenue = mean_revenue_pivot_year.max().max()

    layout = go.Layout(
        title="Average Box Office Revenue per Language over the Years",
        title_x=0.5,
        title_font=dict(family="Arial"),
        xaxis=dict(title="Average Revenue [$]", range=[0, max_revenue * 1.1]),
        yaxis=dict(
            title="Language",
            autorange="reversed",
            categoryorder="array",
            categoryarray=all_languages,
        ),
        template="plotly_white",
        height=600,
        margin=dict(l=100, r=50, t=100, b=50),
        sliders=[
            {
                "active": 0,
                "steps": [
                    {
                        "label": str(year),
                        "method": "animate",
                        "args": [
                            [str(year)],
                            {
                                "frame": {"duration": 800, "redraw": True},
                                "mode": "immediate",
                            },
                        ],
                    }
                    for year in years
                ],
                "x": 0.1,
                "y": -0.1,
                "len": 0.9,
            }
        ],
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 800, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 100, "easing": "linear"},
                            },
                        ],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
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
                "y": -0.1,
                "yanchor": "top",
            }
        ],
    )

    fig = go.Figure(
        data=[
            go.Bar(
                y=all_languages,
                x=[sorted_initial.get(lang, 0) for lang in all_languages],
                orientation="h",
                width=0.8,
                marker=dict(
                    color=[language_color_map[language] for language in all_languages]
                ),
                name="Revenue",
            )
        ],
        layout=layout,
        frames=frames,
    )

    fig.show()

    fig.write_html(
        f"{SAVE_PATH_TONGUES}average_revenue_per_language_per_year.html",
        config={
            "toImageButtonOptions": {
                "filename": "average_revenue_per_language_per_year"
            }
        },
    )


def revenue_per_nbr_languages(df_movie_country_language, mean_language_revenue):
    fig = px.box(
        df_movie_country_language,
        x="nbr_languages",
        y="log_revenue",
        title="Box Office Revenue Distribution per Number of Languages",
        labels={
            "nbr_languages": "Number of Languages",
            "log_revenue": "Logarithmic Revenue [$]",
        },
        category_orders={"nbr_languages": mean_language_revenue},
        color="nbr_languages",
        color_discrete_sequence=px.colors.qualitative.Set2,
        points="outliers",
    )

    fig.update_layout(
        xaxis_title="Number of Languages",
        yaxis_title="Logarithmic Revenue [$]",
        title_x=0.5,
        title_font=dict(family="Arial"),
        xaxis=dict(
            tickmode="linear",
            tick0=1,
            dtick=1,
        ),
        template="plotly_white",
        showlegend=False,
    )

    fig.show()
    fig.write_html(
        f"{SAVE_PATH_TONGUES}revenue_per_nbr_languages.html",
        config={"toImageButtonOptions": {"filename": "revenue_per_nbr_languages"}},
    )


def map_average_revenue_by_country(country_revenue_df):
    fig = px.choropleth(
        country_revenue_df,
        locations="Country",
        locationmode="country names",
        color="Average Box Office Revenue",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.matter,
        title="Average Box Office Revenue by Country",
    )

    fig.update_layout(
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        coloraxis_colorbar=dict(
            title="Average Box Office Revenue [$]",
        ),
        template="plotly_white",
    )

    fig.show()
    fig.write_html(
        f"{SAVE_PATH_TONGUES}map_average_revenue_by_country.html",
        config={"toImageButtonOptions": {"filename": "map_average_revenue_by_country"}},
    )


def country_highest_mean_box_office(df_movie_country_language, top_countries):
    df_movie_country_top = df_movie_country_language[
        df_movie_country_language["first_country"].isin(top_countries.index)
    ]
    movies_per_country_top = df_movie_country_top.groupby("first_country")[
        "movie_name"
    ].nunique()
    movie_counts_aligned = [
        movies_per_country_top.loc[lang] if lang in movies_per_country_top else 0
        for lang in top_countries.index
    ]
    movie_counts_aligned_df = pd.DataFrame(
        movie_counts_aligned, index=top_countries.index
    )
    plot_data_movies = pd.DataFrame(
        {
            "Country": top_countries.index,
            "Average Box Office Revenue [$]": top_countries.values,
            "Movie Count": movie_counts_aligned_df.values.ravel(),
        }
    )

    fig = px.bar(
        data_frame=plot_data_movies,
        x="Country",
        y="Average Box Office Revenue [$]",
        labels={"x": "Country", "y": "Average Box Office Revenue [$]"},
        title=f"Top 10 Countries with Highest Average Box Office Revenue",
        color="Country",
        color_discrete_sequence=px.colors.qualitative.Set2,
        text="Average Box Office Revenue [$]",
        custom_data=["Movie Count"],
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(pad=dict(t=10, b=0)),
        showlegend=False,
        template="plotly_white",
    )

    fig.update_traces(
        texttemplate="%{text:.2s} <br>(%{customdata[0]} movies)",
        textposition="outside",
    )

    fig.update_yaxes(range=[0, max(top_countries.values) * 1.2])

    fig.show()
    fig.write_html(
        f"{SAVE_PATH_TONGUES}country_highest_mean_box_office.html",
        config={
            "toImageButtonOptions": {"filename": "country_highest_mean_box_office"}
        },
    )


def create_treemap(data, title, year, colors, mode="movies", top_n=10):
    year_data = data[data["release_year"] == year]

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
        )
        top_data["movie_name"] = top_data["director"].apply(
            lambda x: year_data[year_data["director"] == x]["movie_name"].tolist()
        )

        top_data["movie_name"] = top_data["movie_name"].apply(
            lambda x: ",".join(x)
        )
    else:
        raise ValueError("Invalid mode. Choose 'movies' or 'directors'.")

    fig = px.treemap(
        top_data,
        path=col_to_path,
        values="inflated_revenue",
        color="director",
        title=f"Top {top_n} {title} Revenues Over the Years",
        labels={"inflated_revenue": "Revenue"},
        color_discrete_sequence=colors,
        hover_data={
            "movie_name": True,
            "director": True,
            "inflated_revenue": ":.2f",
        },
    )
    fig.update_traces(
        hovertemplate="<b>Movie:</b> %{customdata[0]}<br><b>Director:</b> %{customdata[1]}<br><b>Revenue:</b> %{value:$,.0f}",
    )
    fig.update_layout(
        paper_bgcolor="white",
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(pad=dict(t=10, b=0)),
        template="plotly_white",
        title_x=0.5,
    )
    return fig


def create_animated_treemap(
    data,
    title,
    colors,
    speed=2000,
    mode="movies",
    top_n=10,
    start_year=None,
    name="top_15_directors_movie_count.html",
):
    data["release_year"] = data["release_year"].astype(int)

    unique_years = sorted(data["release_year"].unique())

    if start_year is None:
        start_year = unique_years[len(unique_years) // 2]

    frames = [
        go.Frame(
            data=create_treemap(data, title, year, colors, mode=mode, top_n=top_n).data,
            name=str(year),
        )
        for year in unique_years
    ]

    initial_fig = create_treemap(
        data, title, start_year, colors, mode=mode, top_n=top_n
    )
    initial_fig.frames = frames

    initial_fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": speed, "redraw": True},
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
                                "frame": {"duration": 300, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 300},
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
                                "frame": {"duration": speed, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 300},
                            },
                        ],
                        "label": str(year),
                        "method": "animate",
                    }
                    for year in unique_years
                ],
                "active": unique_years.index(start_year),
                "x": 0.1,
                "len": 0.9,
                "xanchor": "left",
                "y": -0.2,
                "yanchor": "top",
            }
        ],
        title_x=0.5,
        title_font=dict(family="Arial"),
        margin=dict(t=70, b=50, l=50, r=50),
        title=dict(pad=dict(t=10, b=0)),
    )
    initial_fig.show()
    initial_fig.write_html(
        f"{SAVE_PATH_STARLIGHT}{name}.html",
        config={"toImageButtonOptions": {"filename": name}},
    )


def interactive_log_revenue(data):
    yearly_data = (
        data.groupby(["release_year", "movie_name", "director"])["inflated_revenue"]
        .max()
        .reset_index()
    )
    yearly_data["log_revenue"] = np.log10(yearly_data["inflated_revenue"])
    yearly_max = yearly_data.loc[
        yearly_data.groupby("release_year")["inflated_revenue"].idxmax()
    ]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=yearly_max["release_year"],
            y=yearly_max["log_revenue"],
            mode="lines+markers",
            marker=dict(size=8, color=px.colors.qualitative.Set2[0]),
            line=dict(width=2),
            name="Logarithmic Max Box Office Revenue",
            hovertemplate="<b>Year:</b> %{x}<br><b>Log Revenue:</b> %{y:.2f}<br><b>Movie:</b> %{customdata[0]}<br><b>Director:</b> %{customdata[1]}<extra></extra>",
            customdata=np.stack(
                (yearly_max["movie_name"], yearly_max["director"]), axis=-1
            ),
        )
    )
    fig.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Logarithmic Box Office Revenue [$]",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=40, b=40),
        title=dict(text="Maximum Box Office Revenue Over Time", pad=dict(t=10, b=0)),
        title_x=0.5,
        title_font=dict(family="Arial"),
    )
    fig.update_xaxes(
        range=[yearly_max["release_year"].min(), yearly_max["release_year"].max()]
    )
    fig.show()
    fig.write_html(
        f"{SAVE_PATH_STARLIGHT}log_max_box_office_revenue_over_time.html",
        config={
            "toImageButtonOptions": {"filename": "log_max_box_office_revenue_over_time"}
        },
    )


def barplot_top_directors_movie_count(data):
    df_count = data
    fig = px.bar(
        df_count,
        x="director",
        y="movie_count",
        text="movie_count",
        title="Top 15 Directors by Number of Movies",
        labels={"director": "Director", "movie_count": "Number of Movies"},
        template="plotly_white",
        color="movie_count",
        color_continuous_scale=px.colors.qualitative.Set2,
    )
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        textfont_size=10,
        hovertemplate="<b>%{x}</b><br>Number of Movies: %{y}",
    )
    fig.update_layout(
        xaxis=dict(tickangle=45),
        margin=dict(l=40, r=20, t=60, b=60),
        coloraxis_showscale=False,
        title_x=0.5,
    )
    fig.show()
    fig.write_html(
        f"{SAVE_PATH_STARLIGHT}top_10_movie_release_countries.html",
        config={"toImageButtonOptions": {"filename": "top_10_movie_release_countries"}},
    )


def race_plot(data, speed=1000):
    df_race = data.sort_values(by="release_year")
    df_race["cumulative_revenue"] = df_race.groupby("director")[
        "inflated_revenue"
    ].cumsum()
    all_years = pd.DataFrame(
        {
            "release_year": range(
                int(df_race.release_year.min()), int(df_race.release_year.max()) + 1
            )
        }
    )
    all_directors = pd.DataFrame({"director": df_race["director"].unique()})
    year_director_grid = all_years.merge(all_directors, how="cross")
    cumulative_df = year_director_grid.merge(
        df_race[["release_year", "director", "cumulative_revenue"]],
        on=["release_year", "director"],
        how="left",
    )
    cumulative_df["cumulative_revenue"] = (
        cumulative_df.groupby("director")["cumulative_revenue"].ffill().fillna(0)
    )
    cumulative_df = (
        cumulative_df.groupby("release_year")
        .apply(lambda group: group.nlargest(15, "cumulative_revenue"))
        .reset_index(drop=True)
    )
    colors = (
        px.colors.qualitative.Set2 * 10 + px.colors.qualitative.Set2[:7]
    )
    color_discrete_map = {
        director: colors[i]
        for i, director in enumerate(cumulative_df["director"].unique())
    }
    cumulative_df["color"] = cumulative_df["director"].map(color_discrete_map)
    colors = cumulative_df["color"].values
    bar = go.barplot(
        df=cumulative_df,
        item_column="director",
        value_column="cumulative_revenue",
        time_column="release_year",
        top_entries=10,
        item_color=colors,
    )
    bar.plot(
        title="Cumulative Revenue of Directors Over Time",
        item_label="Director",
        value_label="Cumulative Revenue [$]",
        frame_duration=speed,
    )
    bar.fig.update_layout(title_x=0.5)
    bar.fig.show()
    bar.fig.write_html(
        f"{SAVE_PATH_STARLIGHT}cumulative_revenue_director_top15_raceplot.html",
        config={
            "toImageButtonOptions": {
                "filename": "cumulative_revenue_director_top15_raceplot"
            }
        },
    )


def total_barplot(data):
    df_top_dir = data
    df_top_dir["total_revenue_billion"] = df_top_dir["total_revenue"] / 1e9
    df_top_dir = df_top_dir.sort_values(
        by="total_revenue_billion", ascending=True
    ).head(15)
    fig = px.bar(
        df_top_dir,
        x="total_revenue_billion",
        y="director",
        text="total_revenue_billion",
        title="Top 15 Directors by Box Office Revenue",
        orientation="h",
        labels={"total_revenue_billion": "Revenue [$]", "director": "Director"},
    )
    fig.update_traces(
        texttemplate="%{text:.2f}B",
        textfont_size=10,
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: %{x:.2f}B",
        marker_color=px.colors.qualitative.Set2 + px.colors.qualitative.Set2[:7],
    )
    max_value = df_top_dir["total_revenue_billion"].max() * 1.1
    fig.update_layout(
        xaxis=dict(
            ticksuffix="B",
            range=[0, max_value],
        ),
        yaxis=dict(tickmode="linear"),
        margin=dict(l=120, r=30, t=60, b=20),
        title_x=0.5,
        template="plotly_white",
    )
    fig.show()
    fig.write_html(
        f"{SAVE_PATH_STARLIGHT}top_15_directors_total_revenue.html",
        config={"toImageButtonOptions": {"filename": "top_15_directors_total_revenue"}},
    )


def create_interactive_scatter_budget_vs_revenue(df):
    fig = px.scatter(
        df,
        x="log_budget",
        y="log_revenue",
        title="Movie Budget vs. Box Office Revenue",
        labels={
            "log_budget": "Logarithmic Inflated Budget",
            "log_revenue": "Logarithmic Inflated Revenue",
        },
        color_discrete_sequence=px.colors.qualitative.Set2,
        hover_data=df.columns,
    )
    fig.update_traces(
        marker=dict(size=10, opacity=0.7),
        hovertemplate="<b>%{customdata[0]}</b><br><br>"
        "Inflated Budget: $%{customdata[1]:,.0f}<br>"
        "Inflated Revenue: $%{customdata[2]:,.0f}<br>"
        "Logarithmic Inflated Budget: %{x}<br>"
        "Logarithmic Inflated Revenue: %{y}<br>"
        "<extra></extra>",
    )
    fig.update_layout(
        xaxis_title="Logarithmic Inflated Budget [$]",
        yaxis_title="Logarithmic Inflated Revenue [$]",
        title=dict(x=0.5),
        title_font=dict(family="Arial"),
        template="plotly_white",
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}scatter_budget_vs_revenue.html",
        config={"toImageButtonOptions": {"filename": "scatter_budget_vs_revenue"}},
    )
    fig.show()


def create_interactive_boxplots_budget_per_genre(df_budget_filtered, top_20_genres):
    fig = px.box(
        df_budget_filtered,
        x="genres_list",
        y="log_budget",
        color="genres_list",
        category_orders={"genres_list": top_20_genres},
        title="Distribution of Budget per Genre (Top 20 Most Common Genres)",
        labels={"genres_list": "Genre", "log_budget": "Log10(Budget)"},
    )
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Logarithmic Budget",
        xaxis_tickangle=45,
        title=dict(x=0.5),
        template="plotly_white",
        showlegend=False,
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}boxplots_budget_per_genre.html",
        config={"toImageButtonOptions": {"filename": "boxplots_budget_per_genre"}},
    )
    fig.show()


def create_interactive_boxplots_ROI_per_genre(df_budget_filtered, top_20_genres):
    fig = px.box(
        df_budget_filtered,
        x="genres_list",
        y="log_ROI",
        color="genres_list",
        category_orders={"genres_list": top_20_genres},
        labels={"genres_list": "Genre", "log_ROI": "Log10(ROI)"},
        title="Distribution of ROI per Genre",
    )
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Logarithmic ROI",
        title=dict(x=0.5),
        template="plotly_white",
        showlegend=False,
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}boxplots_ROI_per_genre.html",
        config={"toImageButtonOptions": {"filename": "boxplots_ROI_per_genre"}},
    )
    fig.show()


def plot_budget_and_revenue_distributions(df, colors, nbins=50):
    log_budget = df["log_budget"]
    log_revenue = df["log_revenue"]
    fig = make_subplots(
        rows=1,
        cols=2,
    )
    fig.add_trace(
        go.Histogram(
            x=log_budget,
            nbinsx=nbins,
            marker=dict(color=colors[2]),
            name="Logarithmic Budget [$]",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Histogram(
            x=log_revenue,
            nbinsx=nbins,
            marker=dict(color=colors[3]),
            name="Logarithmic Revenue [$]",
        ),
        row=1,
        col=2,
    )
    fig.update_layout(
        title_text="Budget and Box Office Revenue Distributions",
        title_x=0.5,
        title_font=dict(family="Arial"),
        template="plotly_white",
        showlegend=False,
    )
    fig.update_xaxes(title_text="Logarithmic Budget [$]", row=1, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=1)
    fig.update_xaxes(title_text="Logarithmic Revenue [$]", row=1, col=2)
    fig.update_yaxes(title_text="Frequency", row=1, col=2)
    fig.write_html(
        f"{SAVE_PATH_TREASURE}budget_and_revenue_distributions.html",
        config={
            "toImageButtonOptions": {"filename": "budget_and_revenue_distributions"}
        },
    )
    fig.show()


def plot_budget_revenue_over_time(df):
    df_budget_trend = df.groupby("release_year").filter(lambda x: len(x) >= 10)
    annual_stats = (
        df_budget_trend.groupby("release_year")
        .agg(
            avg_budget=("inflated_budget", "mean"),
            avg_revenue=("inflated_revenue", "mean"),
        )
        .reset_index()
    )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=annual_stats["release_year"],
            y=annual_stats["avg_budget"],
            mode="lines+markers",
            name="Average Budget",
            line=dict(color="rgb(102,194,165)", width=2.5),
            marker=dict(size=6),
            yaxis="y1",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=annual_stats["release_year"],
            y=annual_stats["avg_revenue"],
            mode="lines+markers",
            name="Average Revenue",
            line=dict(color="rgb(252,141,98)", width=2.5),
            marker=dict(size=6),
            yaxis="y2",
        )
    )
    fig.update_layout(
        title_text=f"Average Budget and Box Office Revenue Over Time",
        title_x=0.5,
        title_font=dict(family="Arial"),
        xaxis=dict(title="Release Year"),
        yaxis=dict(
            title="Average Budget [$]",
            titlefont=dict(color="rgb(102,194,165)"),
            tickfont=dict(color="rgb(102,194,165)"),
            showgrid=True,
            zeroline=True,
        ),
        yaxis2=dict(
            title="Average Revenue [$]",
            titlefont=dict(color="rgb(252,141,98)"),
            tickfont=dict(color="rgb(252,141,98)"),
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="Black",
            borderwidth=1,
        ),
        template="plotly_white",
        showlegend=False,
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}budget_revenue_over_time.html",
        config={"toImageButtonOptions": {"filename": "budget_revenue_over_time"}},
    )
    fig.show()


def plot_roi_distribution(
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
    plot_data = transformation(data[column]) if transformation else data[column]
    hist, bin_edges = np.histogram(plot_data, bins=bins)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=bin_edges[:-1],
            y=hist,
            width=np.diff(bin_edges),
            marker=dict(color=color),
            name="Histogram",
            opacity=0.7,
        )
    )
    if kde:
        from scipy.stats import gaussian_kde

        kde_curve = gaussian_kde(plot_data)
        x_kde = np.linspace(plot_data.min(), plot_data.max(), 500)
        y_kde = kde_curve(x_kde) * len(plot_data) * (bin_edges[1] - bin_edges[0])
        fig.add_trace(
            go.Scatter(
                x=x_kde,
                y=y_kde,
                mode="lines",
                line=dict(color="darkorange", width=2),
                name="KDE",
            )
        )
    fig.update_layout(
        title=title,
        xaxis_title=xlabel if xlabel else column,
        yaxis_title=ylabel,
        title_font=dict(family="Arial"),
        template="plotly_white",
        title_x=0.5,
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}roi_distribution.html",
        config={"toImageButtonOptions": {"filename": f"roi_distribution"}},
    )
    fig.show()


def plot_roi_by_genre(df):
    df_exploded = df.explode("genres_list")
    genre_stats = (
        df_exploded.groupby("genres_list")
        .agg({"ROI": ["mean", "std", "count"]})
        .reset_index()
    )
    genre_stats.columns = ["genre", "mean_roi", "std_roi", "count"]
    genre_stats["ci"] = 1.645 * (genre_stats["std_roi"] / np.sqrt(genre_stats["count"]))
    top_20_genres = genre_stats.nlargest(20, "count").sort_values(
        "mean_roi", ascending=True
    )
    fig = go.Figure()
    set2_colors = px.colors.qualitative.Set2
    color_count = len(top_20_genres)
    repeated_colors = (set2_colors * (color_count // len(set2_colors) + 1))[
        :color_count
    ]
    fig.add_trace(
        go.Bar(
            x=top_20_genres["mean_roi"],
            y=top_20_genres["genre"],
            orientation="h",
            marker=dict(
                color=repeated_colors,
                line=dict(color="rgba(0, 0, 0, 0.5)", width=1),
            ),
            error_x=dict(
                type="data",
                array=top_20_genres["ci"],
                color="black",
                thickness=1.5,
                width=5,
            ),
            name="Average ROI",
            hovertemplate="<b>%{y}</b><br>Average ROI: %{x:.2f}<br>Count: %{customdata}<extra></extra>",
            customdata=top_20_genres["count"],
        )
    )
    fig.update_layout(
        title="Average ROI by Movie Genre with 90% CI",
        title_x=0.5,
        xaxis_title="Average ROI",
        yaxis_title="Movie Genre",
        template="plotly_white",
        title_font=dict(family="Arial"),
        margin=dict(l=100, r=50, t=50, b=50),
        xaxis=dict(gridcolor="rgba(0,0,0,0.1)", zerolinecolor="rgba(0,0,0,0.3)"),
        bargap=0.4,
    )
    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="black")
    fig.write_html(
        f"{SAVE_PATH_TREASURE}roi_by_genre.html",
        config={"toImageButtonOptions": {"filename": f"roi_by_genre"}},
    )
    fig.show()


def plot_roi_per_genre_boxplot(df_budget):
    df_budget_exploded = df_budget.explode("genres_list")
    genre_counts = df_budget_exploded["genres_list"].value_counts()
    top_20_genres = genre_counts.head(20).index.tolist()
    df_budget_filtered = df_budget_exploded[
        df_budget_exploded["genres_list"].isin(top_20_genres)
    ]
    df_budget_filtered["log_ROI"] = np.log10(df_budget_filtered["ROI"] + 1)
    fig = px.box(
        df_budget_filtered,
        x="genres_list",
        y="log_ROI",
        color="genres_list",
        category_orders={"genres_list": top_20_genres},
        title="ROI Distribution per Genre",
        labels={"genres_list": "Genre", "log_ROI": "Logarithmic ROI"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Logarithmic ROI",
        xaxis=dict(tickangle=45),
        showlegend=False,
        template="plotly_white",
        title_x=0.5,
        title_font=dict(family="Arial"),
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}roi_per_genre_boxplot.html",
        config={"toImageButtonOptions": {"filename": "roi_per_genre_boxplot"}},
    )
    fig.show()


def plot_budget_per_genre(df_budget_filtered, top_20_genres):
    fig = px.box(
        df_budget_filtered,
        x="genres_list",
        y="log_budget",
        color="genres_list",
        category_orders={"genres_list": top_20_genres},
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Budget Distribution for the Top 20 Genres",
        labels={"genres_list": "Genre", "log_budget": "Logarithmic Budget [$]"},
    )
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Logarithmic Budget [$]",
        title_font=dict(family="Arial"),
        xaxis=dict(tickangle=45),
        showlegend=False,
        template="plotly_white",
        title_x=0.5,
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}budget_per_genre.html",
        config={"toImageButtonOptions": {"filename": "budget_per_genre"}},
    )
    fig.show()


def plot_revenue_to_budget_ratio(df_budget):
    df_budget["log_revenue_to_budget_ratio"] = np.log10(
        df_budget["inflated_revenue"] / df_budget["inflated_budget"]
    )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_budget["inflated_budget"],
            y=df_budget["log_revenue_to_budget_ratio"],
            mode="markers",
            marker=dict(size=8, color="coral", opacity=0.6),
            name="Movies",
            text=df_budget["movie_name"],
        )
    )
    fig.add_hline(
        y=np.log10(2),
        line=dict(color="black", width=2, dash="dash"),
        annotation_text="Revenue = Budget",
        annotation_position="bottom right",
    )
    fig.add_hline(
        y=np.log10(1.5),
        line=dict(color="red", width=2, dash="dash"),
        annotation_text="Revenue = 0.5 * Budget",
        annotation_position="bottom right",
    )
    fig.add_hline(
        y=np.log10(11),
        line=dict(color="green", width=2, dash="dash"),
        annotation_text="Revenue = 10 * Budget",
        annotation_position="bottom right",
    )
    fig.update_layout(
        title="Relation Between Budget and Revenue-to-Budget Ratio",
        title_x=0.5,
        xaxis=dict(
            title="Logarithmic Budget [$]",
            type="log",
            showgrid=True,
            gridcolor="lightgray",
        ),
        yaxis=dict(
            title="Logarithmic Revenue-to-Budget Ratio",
            showgrid=True,
            gridcolor="lightgray",
        ),
        template="plotly_white",
        title_font=dict(family="Arial"),
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}revenue_to_budget_ratio.html",
        config={"toImageButtonOptions": {"filename": "revenue_to_budget_ratio"}},
    )
    fig.show()


def plot_budget_correlation_per_genre(genre_corrs):
    fig = go.Figure()
    genre_corrs = genre_corrs.sort_values(by="Pearson", ascending=True)
    fig.add_trace(
        go.Bar(
            x=genre_corrs["Pearson"],
            y=genre_corrs.index,
            orientation="h",
            name="Pearson",
            marker_color=px.colors.qualitative.Set2[6],
        )
    )
    fig.add_trace(
        go.Bar(
            x=genre_corrs["Spearman"],
            y=genre_corrs.index,
            orientation="h",
            name="Spearman",
            marker_color=px.colors.qualitative.Set2[7],
        )
    )
    fig.update_layout(
        title_x=0.5,
        title_font=dict(family="Arial"),
        barmode="group",
        title="Correlation Between Budget and Revenue per Genre in Log-Log Scale",
        xaxis_title="Correlation Coefficient",
        yaxis_title="Genre",
        template="plotly_white",
        legend_title="Correlation Type",
        height=800,
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}budget_correlation_per_genre.html",
        config={"toImageButtonOptions": {"filename": "budget_correlation_per_genre"}},
    )
    fig.show()


def plot_budget_vs_revenue(df_budget):
    slope, intercept, r_value, p_value, std_err = linregress(
        df_budget["log_budget"], df_budget["log_revenue"]
    )
    fig = px.density_heatmap(
        df_budget,
        x="log_budget",
        y="log_revenue",
        nbinsx=30,
        nbinsy=30,
        color_continuous_scale="matter",
        title="Relation Between Budget and Revenue",
        labels={
            "log_budget": "Logarithmic Budget [$]",
            "log_revenue": "Logarithmic Revenue [$]",
        },
    )
    x_vals = np.linspace(
        df_budget["log_budget"].min(), df_budget["log_budget"].max(), 100
    )
    y_vals = slope * x_vals + intercept
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            line=dict(color="red", dash="dash"),
            name="Regression",
        )
    )
    stats_text = (
        f"R² = {r_value**2:.3f}<br>Slope = {slope:.3f}<br>p-value = {p_value:.2e}"
    )
    fig.add_annotation(
        x=0.05,
        y=0.95,
        xref="paper",
        yref="paper",
        text=stats_text,
        showarrow=False,
        font=dict(size=12),
        align="left",
        bgcolor="white",
        bordercolor="black",
    )
    fig.update_layout(
        xaxis_title="Logarithmic Budget [$]",
        yaxis_title="Logarithmic Revenue [$]",
        coloraxis_colorbar=dict(title="Count"),
        template="plotly_white",
        showlegend=True,
        title_font=dict(family="Arial"),
        legend=dict(y=1.05),
        title_x=0.5,
    )
    fig.write_html(
        f"{SAVE_PATH_TREASURE}budget_vs_revenue_hexbin.html",
        config={"toImageButtonOptions": {"filename": "budget_vs_revenue_hexbin"}},
    )
    fig.show()
