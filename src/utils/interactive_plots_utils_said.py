import os
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import linregress
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np

SAVE_PATH_TREASURE = "../c1n3mada-datastory/assets/plots/treasure/"


def plot_budget_and_revenue_distributions(df, colors, nbins=50):
    """
    Create an interactive Plotly plot with side-by-side histograms for log10 of inflated budget and revenue.

    Parameters:
    - df (pd.DataFrame): DataFrame containing 'inflated_budget' and 'inflated_revenue' columns.
    - nbins (int): Number of bins for the histograms.

    Returns:
    - None: Displays the plot.
    """
    # Calculate log10 values
    log_budget = df["log_budget"]
    log_revenue = df["log_revenue"]

    # Create subplots
    fig = make_subplots(
        rows=1,
        cols=2,
    )

    # Add budget distribution
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

    # Add revenue distribution
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

    # Layout adjustments
    fig.update_layout(
        title_text="Budget and Box Office Revenue Distributions",
        title_x=0.5,
        title_font=dict(family="Arial"),
        template="plotly_white",
        showlegend=False,
    )

    # Customize axes for subplots
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

    # Show plot
    fig.show()


def plot_budget_revenue_over_time(df):
    """
    Create an interactive Plotly line plot with two y-axes for average budget and revenue.

    Parameters:
    - df (pd.DataFrame): DataFrame containing 'release_year', 'avg_budget', and 'avg_revenue'.

    Returns:
    - None: Displays the interactive plot.
    """
    # Filter years with at least 10 movies
    df_budget_trend = df.groupby("release_year").filter(lambda x: len(x) >= 10)

    # Calculate annual statistics
    annual_stats = (
        df_budget_trend.groupby("release_year")
        .agg(
            avg_budget=("inflated_budget", "mean"),
            avg_revenue=("inflated_revenue", "mean"),
        )
        .reset_index()
    )

    # Create figure with two y-axes
    fig = go.Figure()

    # Average Budget Line (left axis)
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

    # Average Revenue Line (right axis)
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

    # Update layout for twin axes
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
        # todooooooooooo -> remove the legend, however not sure if it is here
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

    # Show the interactive plot
    fig.show()


# todooooooooo -> I don't understand this plotting


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
    """
    Create an interactive histogram with optional KDE curve using Plotly.
    """
    # Transform data if specified
    plot_data = transformation(data[column]) if transformation else data[column]

    # Generate histogram
    hist, bin_edges = np.histogram(plot_data, bins=bins)

    # Create the histogram trace
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

    # Add KDE if specified
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

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=xlabel if xlabel else column,
        yaxis_title=ylabel,
        title_font=dict(family="Arial"),
        template="plotly_white",
        title_x=0.5,
    )

    # Write HTML file
    fig.write_html(
        f"{SAVE_PATH_TREASURE}roi_distribution.html",
        config={"toImageButtonOptions": {"filename": f"roi_distribution"}},
    )

    # Show plot
    fig.show()


# # Add log_ROI column and filter extreme values
# df_budget["log_ROI"] = np.log10(df_budget["ROI"])
# df_budget_filtered = df_budget[(df_budget["log_ROI"] > -5) & (df_budget["log_ROI"] < 5)]

# # Example usage
# plot_distribution_interactive(
#     df_budget_filtered,
#     column="log_ROI",
#     bins=50,
#     kde=True,
#     color="skyblue",
#     title="Distribution of Return on Investment (Logarithmic)",
#     xlabel="Log10(ROI)",
# )


def plot_roi_by_genre(df):
    """
    Create an interactive horizontal bar chart for Average ROI by Genre with 90% Confidence Intervals.

    Parameters:
    - df (pd.DataFrame): DataFrame containing movie ROI data with 'genres_list' and 'ROI'.

    Returns:
    - None: Displays the interactive plot.
    """
    # Explode genres list
    df_exploded = df.explode("genres_list")

    # Calculate genre statistics
    genre_stats = (
        df_exploded.groupby("genres_list")
        .agg({"ROI": ["mean", "std", "count"]})
        .reset_index()
    )
    genre_stats.columns = ["genre", "mean_roi", "std_roi", "count"]

    # Calculate 90% confidence intervals
    genre_stats["ci"] = 1.645 * (genre_stats["std_roi"] / np.sqrt(genre_stats["count"]))

    # Get top 20 genres by count
    top_20_genres = genre_stats.nlargest(20, "count").sort_values(
        "mean_roi", ascending=True
    )

    # Create the interactive plot
    fig = go.Figure()

    # Assign colors from Set2 palette, repeating if necessary
    set2_colors = px.colors.qualitative.Set2
    color_count = len(top_20_genres)
    repeated_colors = (set2_colors * (color_count // len(set2_colors) + 1))[
        :color_count
    ]

    # Add horizontal bars
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

    # Layout customization
    fig.update_layout(
        title="Average ROI by Movie Genre with 90% CI",
        # center the title
        title_x=0.5,
        xaxis_title="Average ROI",
        yaxis_title="Movie Genre",
        template="plotly_white",
        title_font=dict(family="Arial"),
        margin=dict(l=100, r=50, t=50, b=50),
        xaxis=dict(gridcolor="rgba(0,0,0,0.1)", zerolinecolor="rgba(0,0,0,0.3)"),
        bargap=0.4,
    )

    # Add a vertical line at x=0
    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="black")

    fig.write_html(
        f"{SAVE_PATH_TREASURE}roi_by_genre.html",
        config={"toImageButtonOptions": {"filename": f"roi_by_genre"}},
    )

    # Show the interactive plot
    fig.show()


def plot_roi_per_genre_boxplot(df_budget):
    df_budget_exploded = df_budget.explode("genres_list")

    # Filter for top 20 genres
    genre_counts = df_budget_exploded["genres_list"].value_counts()
    top_20_genres = genre_counts.head(20).index.tolist()
    df_budget_filtered = df_budget_exploded[
        df_budget_exploded["genres_list"].isin(top_20_genres)
    ]

    df_budget_filtered["log_ROI"] = np.log10(df_budget_filtered["ROI"] + 1)

    # Create the interactive boxplot using Plotly
    fig = px.box(
        df_budget_filtered,
        x="genres_list",
        y="log_ROI",
        color="genres_list",
        category_orders={"genres_list": top_20_genres},
        title="ROI Distribution per Genre",
        labels={"genres_list": "Genre", "log_ROI": "Logarithmic ROI"},
        color_discrete_sequence=px.colors.qualitative.Set2,  # Set colors to Set2 palette
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Logarithmic ROI",
        xaxis=dict(tickangle=45),
        showlegend=False,
        template="plotly_white",
        title_x=0.5,
        title_font=dict(family="Arial"),
    )

    # write the plot to an HTML file
    fig.write_html(
        f"{SAVE_PATH_TREASURE}roi_per_genre_boxplot.html",
        config={"toImageButtonOptions": {"filename": "roi_per_genre_boxplot"}},
    )

    fig.show()


def plot_budget_per_genre(df_budget_filtered, top_20_genres):
    # Create the interactive boxplot using Plotly
    fig = px.box(
        df_budget_filtered,
        x="genres_list",
        y="log_budget",
        color="genres_list",
        category_orders={"genres_list": top_20_genres},
        color_discrete_sequence=px.colors.qualitative.Set2,  # Use Set2 palette
        title="Budget Distribution for the Top 20 Genres",
        labels={"genres_list": "Genre", "log_budget": "Logarithmic Budget [$]"},
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Logarithmic Budget [$]",
        title_font=dict(family="Arial"),
        xaxis=dict(tickangle=45),
        showlegend=False,
        template="plotly_white",
        title_x=0.5,
    )

    # write the plot to an HTML file
    fig.write_html(
        f"{SAVE_PATH_TREASURE}budget_per_genre.html",
        config={"toImageButtonOptions": {"filename": "budget_per_genre"}},
    )

    fig.show()


def plot_revenue_to_budget_ratio(df_budget):
    # Add new column for log revenue-to-budget ratio
    df_budget["log_revenue_to_budget_ratio"] = np.log10(
        df_budget["inflated_revenue"] / df_budget["inflated_budget"]
    )

    # Create scatter plot using Plotly
    fig = go.Figure()

    # Scatter points for budgets and ratios
    fig.add_trace(
        go.Scatter(
            x=df_budget["inflated_budget"],
            y=df_budget["log_revenue_to_budget_ratio"],
            mode="markers",
            marker=dict(size=8, color="coral", opacity=0.6),
            name="Movies",
            text=df_budget["movie_name"],  # Add movie titles for hover tooltips
        )
    )

    # Add horizontal lines for thresholds
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

    # Customize the layout
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

    # write the plot to an HTML file
    fig.write_html(
        f"{SAVE_PATH_TREASURE}revenue_to_budget_ratio.html",
        config={"toImageButtonOptions": {"filename": "revenue_to_budget_ratio"}},
    )

    fig.show()


def plot_budget_correlation_per_genre(genre_corrs):
    # Assuming genre_corrs is already defined as in your code
    # genre_corrs: DataFrame with 'Pearson' and 'Spearman' columns, index as 'Genre'

    fig = go.Figure()

    # sort by pearson
    genre_corrs = genre_corrs.sort_values(by="Pearson", ascending=True)

    # Add Pearson bar
    fig.add_trace(
        go.Bar(
            x=genre_corrs["Pearson"],
            y=genre_corrs.index,
            orientation="h",
            name="Pearson",
            marker_color=px.colors.qualitative.Set2[6],
        )
    )

    # Add Spearman bar
    fig.add_trace(
        go.Bar(
            x=genre_corrs["Spearman"],
            y=genre_corrs.index,
            orientation="h",
            name="Spearman",
            marker_color=px.colors.qualitative.Set2[7],
        )
    )

    # Update layout for better readability
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

    # write the plot to an HTML file
    fig.write_html(
        f"{SAVE_PATH_TREASURE}budget_correlation_per_genre.html",
        config={"toImageButtonOptions": {"filename": "budget_correlation_per_genre"}},
    )

    fig.show()


def plot_budget_vs_revenue(df_budget):
    # Calculate regression line and statistics
    slope, intercept, r_value, p_value, std_err = linregress(
        df_budget["log_budget"], df_budget["log_revenue"]
    )

    # Create the hexbin plot using Plotly Express
    fig = px.density_heatmap(
        df_budget,
        x="log_budget",
        y="log_revenue",
        nbinsx=30,  # Hexbin size
        nbinsy=30,
        # todoooooooooooooo -> change to rocket if possible (or viridis)
        # color_continuous_scale="peach",
        color_continuous_scale="matter",
        title="Relation Between Budget and Revenue",
        labels={
            "log_budget": "Logarithmic Budget [$]",
            "log_revenue": "Logarithmic Revenue [$]",
        },
    )

    # Add regression line
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

    # Add statistics as an annotation
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

    # Customize layout
    fig.update_layout(
        xaxis_title="Logarithmic Budget [$]",
        yaxis_title="Logarithmic Revenue [$]",
        coloraxis_colorbar=dict(title="Count"),
        template="plotly_white",
        showlegend=True,
        title_font=dict(family="Arial"),
        legend=dict(y=1.05),  # Move legend a bit up
        title_x=0.5,
        height=600,
        width=800,
    )

    # write the plot to an HTML file
    fig.write_html(
        f"{SAVE_PATH_TREASURE}budget_vs_revenue_hexbin.html",
        config={"toImageButtonOptions": {"filename": "budget_vs_revenue_hexbin"}},
    )

    fig.show()
