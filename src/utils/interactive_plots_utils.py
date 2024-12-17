import numpy as np
import plotly.express as px
import plotly.graph_objs as go

# Interactive plots for Shades 
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
        width=1000, height=800,  
        xaxis=dict(tickangle=45),  
    )
    fig.write_html("interactive_plots/shades/revenue_trends_over_time_heatmap.html")
    fig.show()


def create_interactive_genre_ranking_over_time_racing_barplot(mean_revenue_pivot_decade):
    # replace nan with 0
    mean_revenue_pivot_decade = mean_revenue_pivot_decade.fillna(0)
    # generate colors for genres
    genre_colors = px.colors.qualitative.Alphabet
    genre_color_map = {genre: genre_colors[i % len(genre_colors)] for i, genre in enumerate(mean_revenue_pivot_decade.columns)}
    # prepare frames for animation
    decades = mean_revenue_pivot_decade.index.unique()
    frames = []
    for decade in decades:
        sorted_data = mean_revenue_pivot_decade.loc[decade].sort_values(ascending=False)
        frames.append(go.Frame(
            data=[
                go.Bar(
                    y=sorted_data.index,  
                    x=sorted_data.values, 
                    orientation='h',
                    marker=dict(color=[genre_color_map[genre] for genre in sorted_data.index]),
                    name='Revenue'
                )
            ],
            name=str(decade)
        ))
    # initial chart data
    initial_decade = decades[0]
    sorted_initial = mean_revenue_pivot_decade.loc[initial_decade].sort_values(ascending=False)
    # layout configuration with slider
    layout = go.Layout(
        title='Genre Ranking by Average Box Office Revenue per Decade',
        xaxis=dict(title='Revenue', range=[0, mean_revenue_pivot_decade.max().max() * 1.1]),
        yaxis=dict(autorange='reversed', title='Genres'), 
        sliders=[{
            'active': 0,
            'steps': [
                {'label': str(decade),
                'method': 'animate',
                'args': [[str(decade)], {'frame': {'duration': 3000, 'redraw': True},
                                        'mode': 'immediate'}]}
                for decade in decades
            ],
            'x': 0.1, 'y': -0.1, 'len': 0.9
        }],
        updatemenus=[{
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 800, 'redraw': True},
                                    'fromcurrent': True, 'transition': {'duration': 100, 'easing': 'linear'}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1, 'xanchor': 'right',
            'y': -0.1,
            'yanchor': 'top'
        }],
        height=800,
        width=1200,
    )
    # create the figure
    fig = go.Figure(
        data=[
            go.Bar(
                y=sorted_initial.index,
                x=sorted_initial.values,
                orientation='h',
                marker=dict(color=[genre_color_map[genre] for genre in sorted_initial.index]),
                name='Revenue'
            )
        ],
        layout=layout,
        frames=frames,
    )
    fig.write_html("interactive_plots/shades/genre_ranking_over_time_racing_barplot.html")
    fig.show()    