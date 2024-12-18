import os
import numpy as np
import itertools
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# ----------INTERACTIVE PLOTS FOR THE MOVIE TONGUES----------#
SAVE_PATH_TONGUES = "../c1n3mada-datastory/assets/plots/tongues/"


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
