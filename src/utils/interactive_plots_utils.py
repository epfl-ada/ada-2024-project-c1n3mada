import os
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

SAVE_PATH = "../c1n3mada-datastory/assets/plots/shades/"

# Interactive plots for Shades
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
    fig.write_html(f"{SAVE_PATH}number_of_movies_per_genre.html")
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

    fig.write_html(f"{SAVE_PATH}number_of_genres_per_movie.html")
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
        f"{SAVE_PATH}interactive_top_20_genres_with_highest_revenue.html"
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
        f"{SAVE_PATH}interactive_top_20_genres_with_highest_revenue_2.html"
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

    fig.write_html(f"{SAVE_PATH}boxplots_revenue_distribution_top_20.html")
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

    fig.write_html(f"{SAVE_PATH}boxplots_num_genres.html")
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

    fig.write_html(f"{SAVE_PATH}avg_revenue_per_num_genres.html")
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
    fig.write_html(f"{SAVE_PATH}revenue_trends_over_time_heatmap.html")
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
                                "frame": {"duration": 3000, "redraw": True},
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
        f"{SAVE_PATH}genre_ranking_over_time_racing_barplot.html"
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

    fig.write_html(f"{SAVE_PATH}stacked_area_plot_genre_over_time.html")
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

    fig.write_html(f"{SAVE_PATH}heatmap_genre_over_time.html")
    fig.show()
