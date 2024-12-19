import os
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

SAVE_PATH_SHADES = "../c1n3mada-datastory/assets/plots/shades/"
SAVE_PATH_TONGUES = "../c1n3mada-datastory/assets/plots/tongues/"
SAVE_PATH_TREASURE = "../c1n3mada-datastory/assets/plots/treasure/"


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

    # update hover template
    fig.update_traces(
        hovertemplate="<b>Genre:</b> %{x}<br><b>Number of Movies:</b> %{y}<extra></extra>"
    )

    # update layout for readability
    fig.update_layout(
        xaxis_tickangle=45,
        xaxis_title="Genre",
        yaxis_title="Number of Movies",
        template="plotly_white",
        bargap=0.2,
        hovermode="closest",
        showlegend=False,
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
        title="Distribution of Number of Genres per Movie",
        labels={"x": "Number of Genres", "y": "Number of Movies"},
        color=num_genres_distribution.index.astype(str),
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    # update hover template
    fig.update_traces(
        hovertemplate="<b>Number of Genres:</b> %{x}<br><b>Number of Movies:</b> %{y}<extra></extra>"
    )

    # update layout for readability and size
    fig.update_layout(
        xaxis_title="Number of Genres",
        yaxis_title="Number of Movies",
        template="plotly_white",
        bargap=0.2,
        hovermode="closest",
        showlegend=False,
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
        labels={"x": "Genre", "mean": "Average Box Office Revenue ($)"},
        color=top_genres.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        custom_data="count",
    )

    # update hover template
    fig.update_traces(
        hovertemplate=(
            "<b>Genre:</b> %{x}<br>"
            "<b>Average Revenue:</b> $%{y:,.2f}<br>"
            "<b>Number of Movies:</b> %{customdata}"
            "<extra></extra>"
        )
    )

    # update layout
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Average Box Office Revenue ($)",
        xaxis_tickangle=45,
        hovermode="closest",
        template="plotly_white",
        showlegend=False,
    )

    fig.write_html(
        f"{SAVE_PATH_SHADES}interactive_top_20_genres_with_highest_revenue.html",
        config={
            "toImageButtonOptions": {"filename": "top_20_genres_with_highest_revenue"}
        },
    )
    fig.show()


def create_interactive_top_20_genres_with_highest_revenue_2(mean_genre_revenue):
    top_n = 20
    top_genres = mean_genre_revenue.head(top_n)
    fig = px.bar(
        top_genres,
        x=top_genres.index,
        y="mean",
        title=f"Average Revenue per Genre (Top {top_n} Most Common Genres)",
        labels={"x": "Genre", "mean": "Average Box Office Revenue ($)"},
        color=top_genres.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        custom_data="count",
    )

    # update hover template
    fig.update_traces(
        hovertemplate=(
            "<b>Genre:</b> %{x}<br>"
            "<b>Average Revenue:</b> $%{y:,.2f}<br>"
            "<b>Number of Movies:</b> %{customdata}"
            "<extra></extra>"
        )
    )

    # update layout
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Average Box Office Revenue ($)",
        xaxis_tickangle=45,
        hovermode="closest",
        template="plotly_white",
        showlegend=False,
    )

    fig.write_html(
        f"{SAVE_PATH_SHADES}interactive_top_20_genres_with_highest_revenue_2.html",
        config={
            "toImageButtonOptions": {"filename": "top_20_genres_with_highest_revenue_2"}
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

    # update layout for better readability
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

    # update layout for better readability
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

    # update hover template
    fig.update_traces(
        hovertemplate=(
            "<b>Number of Genres:</b> %{x}<br>"
            "<b>Average Revenue:</b> $%{y:,.2f}<extra></extra>"
        )
    )

    # update layout
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
    fig = px.imshow(
        mean_revenue_pivot.T,
        labels=dict(x="Release Year", y="Genre", color="Average Revenue"),
        title="Average Box Office Revenue per Genre Over Time",
        color_continuous_scale="matter",
        aspect="auto",
    )

    fig.update_layout(
        xaxis=dict(tickangle=45),
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
    # replace nan with 0
    mean_revenue_pivot_decade = mean_revenue_pivot_decade.fillna(0)
    # generate colors for genres
    genre_colors = px.colors.qualitative.Alphabet
    genre_color_map = {
        genre: genre_colors[i % len(genre_colors)]
        for i, genre in enumerate(mean_revenue_pivot_decade.columns)
    }
    # prepare frames for animation
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
    # initial chart data
    initial_decade = decades[0]
    sorted_initial = mean_revenue_pivot_decade.loc[initial_decade].sort_values(
        ascending=False
    )
    # layout configuration with slider
    layout = go.Layout(
        title="Genre Ranking by Average Box Office Revenue per Decade",
        xaxis=dict(
            title="Revenue", range=[0, mean_revenue_pivot_decade.max().max() * 1.1]
        ),
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
    # create the figure
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

    # update layout
    fig.update_layout(
        title="Number of Movies per Genre Over Time",
        xaxis_title="Release Year",
        yaxis_title="Number of Movies",
        template="plotly_white",
        legend_title="Genres",
        xaxis=dict(tickangle=45),
        yaxis=dict(gridcolor="rgba(200,200,200,0.5)"),
        hovermode="x unified",
    )

    fig.write_html(
        f"{SAVE_PATH_SHADES}stacked_area_plot_genre_over_time.html",
        config={
            "toImageButtonOptions": {"filename": "stacked_area_plot_genre_over_time"}
        },
    )
    fig.show()


def create_interactive_heatmap_genre_over_time(genre_year_pivot):
    fig = go.Figure(
        data=go.Heatmap(
            z=genre_year_pivot.values,
            x=genre_year_pivot.columns,
            y=genre_year_pivot.index,
            colorscale="matter",
            colorbar=dict(title="Number of Movies"),
            hovertemplate=(
                "<b>Genre:</b> %{y}<br>"
                "<b>Release Year:</b> %{x}<br>"
                "<b>Number of Movies:</b> %{z}<extra></extra>"
            ),
        )
    )

    # update layout
    fig.update_layout(
        title="Number of Movies per Genre Over Time",
        xaxis_title="Release Year",
        yaxis_title="Genre",
        xaxis=dict(tickangle=45),
        template="plotly_white",
    )

    fig.write_html(
        f"{SAVE_PATH_SHADES}heatmap_genre_over_time.html",
        config={"toImageButtonOptions": {"filename": "heatmap_genre_over_time"}},
    )
    fig.show()


def create_interactive_grid(mean_revenue_pivot, genre_year_pivot):
    genres = mean_revenue_pivot.columns.tolist()
    initial_genre = genres[0]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=mean_revenue_pivot.index,
            y=mean_revenue_pivot[initial_genre],
            name="Average Box Office Revenue ($)",
            line=dict(color="blue"),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=genre_year_pivot.index,
            y=genre_year_pivot[initial_genre],
            name="Number of Movies",
            line=dict(color="red"),
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title=f"Genre: {initial_genre}",
        xaxis_title="Year",
        yaxis_title="Average Box Office Revenue ($)",
        yaxis2_title="Number of Movies",
        yaxis2=dict(showgrid=False),
        template="plotly_white",
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
                            },  # update data
                            {"title": f"Genre: {genre}"},  # update title
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
    # filter the dataset to only include the top languages
    df_movie_language_extended_top = df_movie_country_language_extended[
        df_movie_country_language_extended["movie_languages"].isin(top_languages.index)
    ]
    # count the number of movies for these languages (for each language individually)
    movies_per_language_top = df_movie_language_extended_top.groupby("movie_languages")[
        "movie_name"
    ].nunique()
    # align movie counts with the order of top languages index
    movie_counts_aligned = [
        movies_per_language_top.loc[lang] if lang in movies_per_language_top else 0
        for lang in top_languages.index
    ]
    # transform into dataframe (movie_counts_aligned)
    movie_counts_aligned_df = pd.DataFrame(
        movie_counts_aligned, index=top_languages.index
    )
    # transform into dataframe
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
    # pivot the data to prepare for animation
    mean_revenue_pivot_year = filtered_df.pivot(
        index="release_year", columns="movie_languages", values="average_revenue"
    ).fillna(0)
    language_colors = px.colors.qualitative.Set2
    language_color_map = {
        language: language_colors[i % len(language_colors)]
        for i, language in enumerate(mean_revenue_pivot_year.columns)
    }
    # always show all languages
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

    # fix the axis based on the overall max value
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
    # filter the dataset to only include the top countries
    df_movie_country_top = df_movie_country_language[
        df_movie_country_language["first_country"].isin(top_countries.index)
    ]
    # count the number of movies for these top countries (for each country individually)
    movies_per_country_top = df_movie_country_top.groupby("first_country")[
        "movie_name"
    ].nunique()
    # align movie counts with the order of top languages index
    movie_counts_aligned = [
        movies_per_country_top.loc[lang] if lang in movies_per_country_top else 0
        for lang in top_countries.index
    ]
    # transform into dataframe (movie_counts_aligned)
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


## ----------INTERACTIVE PLOTS FOR THE MOVIE TREASURE----------#


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
