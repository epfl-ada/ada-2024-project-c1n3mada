import plotly.graph_objects as go
import plotly.express as px
import scipy.stats as stats
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

SAVE_PATH_ECHO = "../c1n3mada-datastory/assets/plots/echo/"


def plot_num_of_movies_per_genre(df_rating):
    # Explode the genres_list to count each genre separately
    genre_counts = df_rating.explode("genres_list")["genres_list"].value_counts()

    # Get the most common 20 genres
    genre_counts_top20 = genre_counts.head(20).reset_index()
    genre_counts_top20.columns = ["Genre", "Number of Movies"]

    # Create an interactive bar plot using Plotly
    fig = px.bar(
        genre_counts_top20,
        x="Genre",
        y="Number of Movies",
        color="Genre",
        title="Number of Movies per Genre",
        text="Number of Movies",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    # Update layout for better aesthetics
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

    # Add interactivity improvements
    fig.update_traces(
        texttemplate="%{text}",
        # textposition="outside",
        hovertemplate="<b>Genre:</b> %{x}<br><b>Number of Movies:</b> %{y}<extra></extra>",
    )

    # Save the plot as an HTML file
    fig.write_html(
        f"{SAVE_PATH_ECHO}num_movies_per_genre.html",
        config={"toImageButtonOptions": {"filename": "num_movies_per_genre"}},
    )

    fig.show()


def plot_imdb_rating_distribution(df_rating):
    # Colorblind-friendly and pleasing color
    # set2 colors
    colors = px.colors.qualitative.Set2
    color = colors[0]

    # Calculate histogram data with custom bins (adjust bin size as needed)
    bins = [
        i / 2 for i in range(2, 100)
    ]  # Example: bins from 1 to 10 with 0.5 increments
    counts, bin_edges = np.histogram(df_rating["averageRating"], bins=bins)

    # Create the histogram trace
    histogram_trace = go.Histogram(
        x=df_rating["averageRating"],
        histnorm="",  # Crucial: Prevents normalization, shows raw counts
        nbinsx=len(bins),
        marker=dict(color=color, line=dict(width=1, color="darkgray")),  # Nice outline
        opacity=0.75,
        # give the trace a name
        name="Histogram",
    )
    fig = go.Figure(data=[histogram_trace])

    # Calculate KDE data if you want to include the curve

    kde = stats.gaussian_kde(df_rating["averageRating"])
    x_range = np.linspace(
        df_rating["averageRating"].min(), df_rating["averageRating"].max(), 100
    )

    kde_trace = go.Scatter(
        x=x_range,
        y=kde(x_range)
        * len(df_rating["averageRating"])
        / 10,  # Scale KDE to match histogram counts
        mode="lines",
        line=dict(color="#808080", width=2),  # Black line for KDE
        name="KDE",  # Label the KDE line
    )

    fig.add_trace(kde_trace)

    # Customize the layout
    fig.update_layout(
        title_text="IMDb Ratings Distribution",
        # center the title text
        title_x=0.5,
        xaxis_title_text="IMDb Rating",
        yaxis_title_text="Number of Movies",
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.01,  # Adjust spacing between bars
        font_color="black",
        xaxis=dict(showgrid=False),  # Black axis titles
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
        ),  # Light gray grid and black axis titles
        title_font=dict(family="Arial"),
        # show the legend for histogram and KDE
        template="plotly_white",
        showlegend=False,
    )

    # Save the plot as an HTML file
    fig.write_html(
        f"{SAVE_PATH_ECHO}imdb_rating_distribution.html",
        config={"toImageButtonOptions": {"filename": "imdb_rating_distribution"}},
    )

    fig.show()


def plot_box_office_revenue_distribution(df_rating):
    # Calculate log10 of revenue
    log_revenue = np.log10(df_rating["inflated_revenue"])

    # Colorblind-friendly and pleasing color
    colors = px.colors.qualitative.Set2
    color = colors[1]

    # Create histogram trace
    histogram_trace = go.Histogram(
        x=log_revenue,
        histnorm="",  # for showing the frequency
        nbinsx=100,  # Adjust number of bins as needed
        marker=dict(color=color, line=dict(width=1, color="darkgray")),
        opacity=0.75,
        name="Histogram",
    )

    fig = go.Figure(data=[histogram_trace])

    # Calculate KDE
    kde = stats.gaussian_kde(log_revenue)
    x_range = np.linspace(log_revenue.min(), log_revenue.max(), 200)  # Smoother curve

    kde_trace = go.Scatter(
        x=x_range,
        y=kde(x_range) * len(log_revenue) / 10,  # Scale KDE to histogram
        mode="lines",
        line=dict(color="#808080", width=2),
        name="KDE",
    )

    fig.add_trace(kde_trace)

    # Customize layout
    fig.update_layout(
        title_text="Box Office Revenue Distribution",
        title_x=0.5,
        xaxis_title_text="Logarithmic Box Office Revenue [$]",
        yaxis_title_text="Number of Movies",  # Frequency label
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

    # Save the plot as an HTML file
    fig.write_html(
        f"{SAVE_PATH_ECHO}box_office_revenue_distribution.html",
        config={
            "toImageButtonOptions": {"filename": "box_office_revenue_distribution"}
        },
    )

    fig.show()


def plot_imdb_rating_vs_box_office_revenue_v1(df_rating):
    # Calculate log10 of revenue
    df_rating["log_revenue"] = np.log10(df_rating["inflated_revenue"])

    # Create the scatter plot
    fig = px.scatter(
        df_rating,
        x="averageRating",
        y="log_revenue",
        hover_data=["movie_name"],  # Show movie name on hover
        title="IMDb Rating vs. Log10 of Box Office Revenue",
        labels={
            "averageRating": "IMDb Rating",
            "log_revenue": "Log10 of Box Office Revenue",
        },
        opacity=0.8,  # Slightly reduce opacity for better readability when points overlap
        color_discrete_sequence=["#0072B2"],  # Consistent color
    )

    # Customize layout for readability
    fig.update_layout(
        xaxis_title="IMDb Rating",
        yaxis_title="Log10 of Box Office Revenue",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="black",
        xaxis=dict(
            showgrid=False, title_font=dict(size=18, color="black")
        ),  # Black x-axis title
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
            title_font=dict(size=18, color="black"),
        ),  # Gray grid, black y-axis title
        title=dict(font=dict(size=24, color="black")),
        hovermode="closest",  # Show hover info only for the closest point
    )

    # Increase marker size and add outline for better visibility
    fig.update_traces(
        marker=dict(
            size=8, line=dict(width=1, color="darkgray")
        ),  # Larger markers with outlines
    )

    # Save the plot as an HTML file
    fig.write_html(
        f"{SAVE_PATH_ECHO}imdb_rating_vs_box_office_revenue.html",
        config={
            "toImageButtonOptions": {"filename": "imdb_rating_vs_box_office_revenue"}
        },
    )

    fig.show()


def plot_imdb_rating_vs_box_office_revenue(df_rating):
    # Create an interactive scatter plot using Plotly
    fig = px.scatter(
        df_rating,
        x="averageRating",
        y=np.log10(df_rating["inflated_revenue"]),
        hover_data=["movie_name", "inflated_revenue"],
        labels={
            "averageRating": "IMDb Rating",
            "y": "Logarithmic Box Office Revenue [$]",
            "inflated_revenue": "Box Office Revenue",
            "movie_name": "Movie Name",
        },
        title="Relation Between IMDb Rating and Box Office Revenue",
        color="averageRating",  # Optional: Color by IMDb rating for better aesthetics
        color_continuous_scale="viridis_r",  # Color-blind friendly palette
        opacity=0.7,  # Make overlapping points more readable
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis=dict(
            title="IMDb Rating",
        ),
        yaxis=dict(
            title="Logarithmic Box Office Revenue [$]",
        ),
        title_font=dict(family="Arial"),
        title_x=0.5,
        template="plotly_white",
    )

    # Add hovertemplate for precise control over displayed information
    fig.update_traces(
        hovertemplate="<b>Movie Name:</b> %{customdata[0]}<br>"
        "<b>IMDb Rating:</b> %{x}<br>"
        "<b>Box Office Revenue:</b> %{customdata[1]:,.0f}<extra></extra>"
    )

    # Save the plot as an HTML file
    fig.write_html(
        f"{SAVE_PATH_ECHO}imdb_rating_vs_box_office_revenue.html",
        config={
            "toImageButtonOptions": {"filename": "imdb_rating_vs_box_office_revenue"}
        },
    )

    # Show the interactive scatter plot
    fig.show()


def plot_correlation_matrix(df_rating):

    custom_labels = {
        "averageRating": "Rating",
        "inflated_revenue": "Revenue",
        "numVotes": "Nbr of Votes",
    }
    # Calculate correlation matrix
    renamed_columns = [
        custom_labels[col]
        for col in df_rating[["averageRating", "inflated_revenue", "numVotes"]].columns
    ]
    corr_matrix = df_rating[["averageRating", "inflated_revenue", "numVotes"]].corr()
    corr_matrix.columns = renamed_columns
    corr_matrix.index = renamed_columns

    # Create the heatmap
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

    # Enforce square aspect ratio
    fig.update_layout(
        title_text="Correlation Between Rating, Revenue and Number of Votes",
        # xaxis_title="Features",
        # yaxis_title="Features",
        plot_bgcolor="white",
        paper_bgcolor="white",
        # font_color="black",
        title_x=0.5,
        xaxis=dict(showgrid=False, constrain="domain"),  # Fix x-axis to make it square
        yaxis=dict(
            showgrid=False, scaleanchor="x", scaleratio=1
        ),  # Match y-axis scale to x-axis
        # add "Correlation score" name to the score bar
        coloraxis=dict(colorbar=dict(title="Correlation Score")),
        title_font=dict(family="Arial"),
    )

    # Save the plot as an HTML file
    fig.write_html(
        f"{SAVE_PATH_ECHO}correlation_matrix.html",
        config={"toImageButtonOptions": {"filename": "correlation_matrix"}},
    )

    fig.show()


def plot_genre_correlation(genre_corrs):
    # Sort values for better visualization
    genre_corrs_sorted = genre_corrs.sort_values("Pearson", ascending=True)

    # Colorblind-friendly colors
    # pearson_color = "#0072B2"  # Bluish
    # spearman_color = "#D55E00"  # Orangish

    colors = px.colors.qualitative.Set2

    pearson_color = colors[6]
    spearman_color = colors[7]

    # Create bar traces
    pearson_trace = go.Bar(
        y=genre_corrs_sorted.index,
        x=genre_corrs_sorted["Pearson"],
        orientation="h",
        name="Pearson",
        marker_color=pearson_color,
        # text=genre_corrs_sorted["Pearson"].round(3),  # Show values on bars
        # textposition="inside",  # Show value labels inside bars if they fit, otherwise auto
        hovertemplate="<b>Genre: %{y}</b><br>Pearson Correlation: %{x:.3f}",  # Custom hover text
    )

    spearman_trace = go.Bar(
        y=genre_corrs_sorted.index,
        x=genre_corrs_sorted["Spearman"],
        orientation="h",
        name="Spearman",
        marker_color=spearman_color,
        # text=genre_corrs_sorted["Spearman"].round(3),
        # textposition="inside",
        hovertemplate="<b>Genre: %{y}</b><br>Spearman Correlation: %{x:.3f}",
    )

    # Create the figure
    fig = go.Figure(data=[pearson_trace, spearman_trace])

    # Update layout
    fig.update_layout(
        title_text="Correlation between IMDb Ratings and Box Office Revenue per Genre",
        xaxis_title="Correlation Coefficient",
        yaxis_title="Genre",
        plot_bgcolor="white",
        paper_bgcolor="white",
        # font_color="black",
        xaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
            zeroline=True,
            zerolinecolor="gray",
        ),
        yaxis=dict(
            showgrid=False,
            autorange="reversed",
        ),  # Reverse y-axis for better readability
        legend=dict(title="Correlation Type"),  # Clear legend title
        barmode="group",  # Show Pearson and Spearman side-by-side
        bargap=0.2,  # Increase gap between Pearson and Spearman bars within a group
        bargroupgap=0.1,  # Increase gap between genre groups
        # Remove default margins
        margin=dict(l=0, r=0, t=40, b=0),  # Adjust top margin for title
        title_font=dict(family="Arial"),
        template="plotly_white",
        title_x=0.5,
    )

    # Save the plot as an HTML file
    fig.write_html(
        f"{SAVE_PATH_ECHO}genre_correlation.html",
        config={"toImageButtonOptions": {"filename": "genre_correlation"}},
    )

    fig.show()


def plot_3d_regression_plane(df_rating, model_multi):
    # Create a meshgrid for plotting
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

    # Actual data points
    actual_x = df_rating["averageRating"]
    actual_y = np.log10(df_rating["numVotes"])
    actual_z = np.log10(df_rating["inflated_revenue"])

    # Create the 3D scatter plot for actual data points
    scatter = go.Scatter3d(
        x=actual_x,
        y=actual_y,
        z=actual_z,
        mode="markers",
        marker=dict(
            size=5,
            color=actual_z,  # Color by revenue for better insight
            colorscale="Viridis_r",  # Color-blind friendly palette
            opacity=0.7,
        ),
        name="Actual Data",
        hovertemplate="<b>IMDb Rating:</b> %{x:.2f}<br>"
        "<b>Log10 NumVotes:</b> %{y:.2f}<br>"
        "<b>Log10 Revenue:</b> %{z:.2f}<br>"
        "<b>Movie:</b> %{text}<extra></extra>",  # Show movie name on hover
        text=df_rating["movie_name"],  # Show movie name on hover
    )

    # Create the regression plane
    surface = go.Surface(
        x=averageRating_range,
        y=log_numVotes_range,
        z=predicted_revenue,
        colorscale="Reds",
        opacity=0.7,
        name="Regression Plane",
        showscale=False,
        hoverinfo="skip",  # Hide hover info for the surface
    )

    # Combine the scatter and surface plots
    fig = go.Figure(data=[scatter, surface])

    # Update layout for aesthetics
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
        margin=dict(l=0, r=0, b=0, t=40),  # Adjust margins for better fit
        template="plotly_white",
        title_font=dict(family="Arial"),
    )

    # Save the plot as an HTML file
    fig.write_html(
        f"{SAVE_PATH_ECHO}3d_regression_plane.html",
        config={"toImageButtonOptions": {"filename": "3d_regression_plane"}},
    )

    # Show the interactive 3D plot
    fig.show()


def plot_hexbin_regression_plane(df_rating):
    # Pre-calculate log revenue
    df_rating["log_revenue"] = np.log10(df_rating["inflated_revenue"])

    # Calculate the trendline (do this once, outside the figure creation)
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

    hexbin_trace = go.Histogram2d(  # Use Histogram2d for hexbins
        x=df_rating["averageRating"],
        y=df_rating["log_revenue"],
        colorscale="Viridis_r",
        nbinsx=50,
        nbinsy=50,
        showscale=True,
        colorbar=dict(
            title="Number of Movies", len=0.5, y=0.25
        ),  # Adjusted colorbar position
        hovertemplate="IMDb Rating: %{x:.2f}<br>Log Revenue: %{y:.2f}<br>Count: %{z}",
        name="bin",
    )

    # Create the marginal distributions with reduced thickness
    x_hist = go.Histogram(
        x=df_rating["averageRating"],
        marker_color="#D3D3D3",  # Or any color you prefer
        opacity=0.75,
        # Adjusted thickness
        marker_line=dict(width=0.07, color="black"),
        yaxis="y2",
        showlegend=False,
        nbinsx=100,  # Number of bins for smooth distribution
        autobinx=False,  # prevents plotly from automatically calculating bins
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
        title_x=0.5,  # Center the title
        title_font=dict(family="Arial"),
        xaxis_title="IMDb Rating",
        yaxis_title="Logarithmic Box Office Revenue [$]",
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            domain=[0, 0.93],
            showgrid=False,
            showticklabels=True,
        ),  # Main x-axis
        yaxis=dict(
            domain=[0, 0.9],
            showgrid=True,
            gridcolor="lightgray",
            showticklabels=True,
        ),  # Main y-axis
        xaxis2=dict(
            domain=[0.93, 1], showgrid=False, showticklabels=False
        ),  # Marginal x-axis (top)
        yaxis2=dict(
            domain=[0.9, 1], showgrid=False, showticklabels=False
        ),  # Marginal y-axis (right)
        # font_color="black",
        margin=dict(t=50, b=0, l=70, r=0),  # Adjusted margins for labels
        legend=dict(
            font=dict(size=12), orientation="h", y=1, x=0.9
        ),  # Legend placement
        # ... (annotations as before) ...
        barmode="overlay",
        bargap=0,
        template="plotly_white",
    )

    # Add trendline and marginal plots last to overlay correctly
    fig = go.Figure(data=[hexbin_trace, trendline_trace, x_hist, y_hist], layout=layout)

    # Save the plot as an HTML file
    fig.write_html(
        f"{SAVE_PATH_ECHO}hexbin_regression_plane.html",
        config={"toImageButtonOptions": {"filename": "hexbin_regression_plane"}},
    )

    fig.show()
