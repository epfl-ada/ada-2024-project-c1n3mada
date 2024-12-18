import os
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

SAVE_PATH_SHADES = "../c1n3mada-datastory/assets/plots/shades/"
SAVE_PATH_BUDGET = "../c1n3mada-datastory/assets/plots/budget/"


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
        go.Scatter(x=mean_revenue_pivot.index, y=mean_revenue_pivot[initial_genre], name='Average Box Office Revenue ($)', line=dict(color='blue')),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=genre_year_pivot.index, y=genre_year_pivot[initial_genre], name='Number of Movies', line=dict(color='red')),
        secondary_y=True
    )

    fig.update_layout(
        title=f"Genre: {initial_genre}",
        xaxis_title='Year',
        yaxis_title='Average Box Office Revenue ($)',
        yaxis2_title='Number of Movies',
        yaxis2=dict(showgrid=False),
        template='plotly_white'
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
                            {"y": [mean_revenue_pivot[genre], genre_year_pivot[genre]]},  # update data
                            {"title": f"Genre: {genre}"}  # update title
                        ]
                    ) for genre in genres
                ],
                x=0,
                y=-0.2,
                xanchor='left',
                yanchor='top',
                direction='up'
            ),
            dict(
                active=2,
                buttons=[
                    dict(
                        label='Revenue',
                        method='update',
                        args=[{"visible": [True, False]}]
                    ),
                    dict(
                        label='Count',
                        method='update',
                        args=[{"visible": [False, True]}]
                    ),
                    dict(
                        label='Both',
                        method='update',
                        args=[{"visible": [True, True]}]
                    )
                ],
                x=0.3,
                y=-0.2,
                xanchor='left',
                yanchor='top',
                direction='up'
            )
        ],
    )

    fig.write_html(
        f"{SAVE_PATH_SHADES}grid.html",
        config={"toImageButtonOptions": {"filename": "grid"}},
    )
    fig.show()


# Interactive plots for Budget
def create_interactive_scatter_budget_vs_revenue(df):
    fig = px.scatter(
        df,
        x="log_budget",
        y="log_revenue",
        title="Movie Budget vs. Box Office Revenue",
        labels={"log_budget": "Logarithmic Inflated Budget", "log_revenue": "Logarithmic Inflated Revenue"},
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
                      "<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Logarithmic Inflated Budget ($)",
        yaxis_title="Logarithmic Inflated Revenue ($)",
        title=dict(x=0.5),
        template="plotly_white",
    )

    fig.write_html(
        f"{SAVE_PATH_BUDGET}scatter_budget_vs_revenue.html",
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
        f"{SAVE_PATH_BUDGET}boxplots_budget_per_genre.html",
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
        f"{SAVE_PATH_BUDGET}boxplots_ROI_per_genre.html",
        config={"toImageButtonOptions": {"filename": "boxplots_ROI_per_genre"}},
    )
    
    fig.show()    
