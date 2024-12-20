SAVE_PATH_DIR = "../c1n3mada-datastory/assets/plots/starlight/"
import plotly.express as px
import plotly.graph_objects as go
from raceplotly.plots import barplot
import pandas as pd
def create_treemap(data, title, year,colors, mode="movies", top_n=10):
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
    year_data = data[data['release_year'] == year] # filter data for the given year

    if mode == "movies":
        col_to_path = ['movie_name']
        top_data= year_data.nlargest(top_n, 'inflated_revenue')[['movie_name', 'director', 'inflated_revenue']].reset_index()
        

    elif mode == "directors":
        col_to_path = ['director']
        top_data = year_data.groupby('director')['inflated_revenue'].sum().nlargest(top_n).reset_index() # group by director and sum the revenue
        top_data['movie_name'] = top_data['director'].apply(
            lambda x: year_data[year_data['director'] == x]['movie_name'].tolist()
        )
        
        top_data['movie_name'] = top_data['movie_name'].apply(lambda x: ','.join(x)) # join the movie names to a single string
    else:
        raise ValueError("Invalid mode. Choose 'movies' or 'directors'.")

    # interactive treemap
    fig = px.treemap(
        top_data,
        path=col_to_path,  
        values='inflated_revenue',  
        color='director',  #
        title=f"Top {top_n} {title} Revenue over the Years",
        labels={'inflated_revenue': 'Revenue'},
        color_discrete_sequence=colors,
        hover_data={'movie_name': True, 'director': True, 'inflated_revenue': ':.2f'},  # Custom hover data
    )
    fig.update_traces(
        hovertemplate="<b>Movie:</b> %{customdata[0]}<br><b>Director:</b> %{customdata[1]}<br><b>Revenue:</b> %{value:$,.0f}",)
    # Common layout customization
    fig.update_layout(
        title=dict(font=dict(size=20), x=0.5),
        paper_bgcolor="white", 
        font=dict(color="black"),  
    )
    return fig


def create_animated_treemap(data, title,colors,speed=1000,mode="movies", top_n=10, start_year=None,name="top_15_directors_movie_count.html"):
    """
    Create an animated treemap with a slider for each year.

    Args:
        data: DataFrame containing movie data
        title: Title for the treemap
        mode: "movies" or "directors" for treemap type
        top_n: Number of top entries to include per year
        start_year: Year to start the animation (default is the middle year)
    
    Returns:
        Plotly figure with animation
    """
    unique_years = sorted(data['release_year'].unique())

    # Set start year to middle year if not provided
    if start_year is None:
        start_year = unique_years[len(unique_years) // 2]

    # Create frames for each year
    frames = [
        go.Frame(
            data=create_treemap(data, title, year,colors, mode=mode, top_n=top_n).data,
            name=str(year)
        )
        for year in unique_years
    ]

    # Create initial plot for the specified start year
    initial_fig = create_treemap(data, title, start_year, colors,mode=mode, top_n=top_n)
    initial_fig.frames = frames

    # Add controls for animation
    initial_fig.update_layout(
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": speed, "redraw": True}, "fromcurrent": True}],
                    "label": "Play",
                    "method": "animate",
                },
                {
                    "args": [[None], {"frame": {"duration": 100, "redraw": True}, "mode": "immediate", "transition": {"duration": 100}}],
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
        }],
        sliders=[{
            "steps": [
                {
                    "args": [[str(year)], {"frame": {"duration": speed, "redraw": True}, "mode": "immediate", "transition": {"duration": 300}}],
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
        }],
        title_x=0.5,
    )
    initial_fig.show()
    initial_fig.write_html(f"{SAVE_PATH_DIR}{name}.html",
        config={"toImageButtonOptions": {"filename": name}},)
    
def interactive_log_revenue(data):
    yearly_inflated_avg = data.groupby("release_year")["log_inflated_revenue"].mean()
    # implement plotly interactive plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly_inflated_avg.index, 
        y=yearly_inflated_avg.values,
        mode='lines+markers',
        marker=dict(size=6, color='blue'),
        line=dict(width=2),
        hoverinfo='x+y',
        name='Log Max Box Office Revenue',
        marker_color=px.colors.qualitative.Set2[0]
    ))

    fig.update_layout(
        title="Log Max Box Office Revenue Over Time",
        xaxis_title="Release Year",
        yaxis_title="Log Box Office Revenue",
        template="plotly",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=40, b=40),
        title_x=0.5,
    )
    #y_lim to not make the plot too big and have empty space
    fig.update_xaxes(range=[1913, 2017])

    fig.update_xaxes(tickangle=45, tickfont=dict(size=10))

    fig.show()
    # save the figure as an HTML file
    fig.write_html(
        f"{SAVE_PATH_DIR}log_max_box_office_revenue_over_time.html",
        config={"toImageButtonOptions": {"filename": "log_max_box_office_revenue_over_time"}},
    )
    
def barplot_top_directors_movie_count(data):
    df_count = data
    # Create interactive bar chart
    fig = px.bar(
        df_count,
        x="director",
        y="movie_count",
        text="movie_count",  # Display values directly on the bars
        title="Top 15 Directors by Number of Movies",
        labels={"director": "Director", "movie_count": "Number of Movies"},
        template="plotly_white",
        color="movie_count",  # Color based on movie count
        color_continuous_scale=px.colors.qualitative.Set2,
    )

    # Customize the trace
    fig.update_traces(
        texttemplate='%{text}',  # Display numbers on bars
        textposition='outside',  # Position labels above the bars
        hovertemplate="<b>%{x}</b><br>Number of Movies: %{y}",  # Customize hover tooltip
    )

    # Layout adjustments
    fig.update_layout(
        xaxis=dict(tickangle=45),  # Rotate x-axis ticks
        margin=dict(l=40, r=20, t=60, b=60),
        coloraxis_showscale=False,  # Hide color scale bar
        title_x=0.5,  # Center title
    )

    # Show interactive plot
    fig.show()
    fig.write_html(f"{SAVE_PATH_DIR}top_10_movie_release_countries.html",
        config={"toImageButtonOptions": {"filename": "top_10_movie_release_countries"}},)

def race_plot(data, speed=1000):
    
    df_race = data.sort_values(by="release_year")
    df_race["cumulative_revenue"] = df_race.groupby("director")["inflated_revenue"].cumsum()

    all_years = pd.DataFrame({"release_year": range(int(df_race.release_year.min()), int(df_race.release_year.max()) + 1)})
    all_directors = pd.DataFrame({"director": df_race["director"].unique()})
    year_director_grid = all_years.merge(all_directors, how="cross")  

    # merge cumulative data into the year-director grid
    cumulative_df = year_director_grid.merge(
        df_race[["release_year", "director", "cumulative_revenue"]],
        on=["release_year", "director"],
        how="left"
    )

    # forward fill and replace missing cumulative revenue with 0
    cumulative_df["cumulative_revenue"] = cumulative_df.groupby("director")["cumulative_revenue"].ffill().fillna(0)

    # dynamically filter top directors year-by-year
    cumulative_df = cumulative_df.groupby("release_year").apply(
        lambda group: group.nlargest(15, "cumulative_revenue")
    ).reset_index(drop=True)
    colors = px.colors.qualitative.Set2*10+px.colors.qualitative.Set2[:7] # no idea how the library handle colors but this is the best I could do
    #print(len(cumulative_df["director"].unique()))
    color_discrete_map = {director: colors[i] for i, director in enumerate(cumulative_df["director"].unique())}
    cumulative_df["color"] = cumulative_df["director"].map(color_discrete_map)
    colors=cumulative_df["color"].values
    # create the animated bar chart race
    bar = barplot(
        df=cumulative_df,
        item_column="director",
        value_column="cumulative_revenue",
        time_column="release_year",
        top_entries=10 ,
        item_color=colors,
    )

    # plot the animation with extended duration
    bar.plot(
        title="Cumulative Revenue of Directors Over Time",
        item_label="Director",
        value_label="Cumulative Revenue [$]",
        frame_duration=speed,
    )

    #bar.fig.update_traces(marker_color=px.colors.qualitative.Set2)
    bar.fig.update_layout(title_x=0.5)
    bar.fig.show()
    bar.fig.write_html(f"{SAVE_PATH_DIR}cumulative_revenue_director_top15_raceplot.html",
        config={"toImageButtonOptions": {"filename": "cumulative_revenue_director_top15_raceplot"}},)

def total_barplot(data):
    # Create interactive bar chart
    df_top_dir = data
    df_top_dir["total_revenue_billion"] = df_top_dir["total_revenue"] / 1e9
    df_top_dir = df_top_dir.sort_values(by="total_revenue_billion", ascending=True).head(15)
    fig = px.bar(
        df_top_dir,
        x="total_revenue_billion",
        y="director",
        text="total_revenue_billion",
        title="Top 15 Directors by Box Office Revenue in Billions",
        orientation="h",
        
        labels={"total_revenue_billion": "Revenue (Billions)", "director": "Director"},
        template="plotly_white",
    )

    # Customize hover tooltips
    fig.update_traces(
        texttemplate='%{text:.2f}B',
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Revenue: %{x:.2f}B",
        marker_color=px.colors.qualitative.Set2+px.colors.qualitative.Set2[:7]
    )

    # Remove unnecessary gridlines and adjust layout
    fig.update_layout(
        xaxis_visible=False,  # Remove x-axis line
        yaxis=dict(tickmode="linear"),
        margin=dict(l=100, r=20, t=60, b=20),
        title_x=0.5,
    )

    # Show interactive plot
    fig.show()
    fig.write_html(
        f"{SAVE_PATH_DIR}top_15_directors_total_revenue.html",
        config={"toImageButtonOptions": {"filename": "top_15_directors_total_revenue"}},
    )
