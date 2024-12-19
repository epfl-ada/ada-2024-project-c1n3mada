import os
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy.stats import linregress

SAVE_PATH = "../c1n3mada-datastory/assets/plots/budget/"


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
            marker=dict(color=colors[0]),
            name="Logarithmic Budget",
        ),
        row=1,
        col=1,
    )

    # Add revenue distribution
    fig.add_trace(
        go.Histogram(
            x=log_revenue,
            nbinsx=nbins,
            marker=dict(color=colors[1]),
            name="Logarithmic Revenue",
        ),
        row=1,
        col=2,
    )

    # Layout adjustments
    fig.update_layout(
        title_text="Budget and Inflated Revenue Distributions",
        title_x=0.5,
        template="plotly_white",
        showlegend=False,
    )

    # Customize axes for subplots
    fig.update_xaxes(title_text="Log10(Budget)", row=1, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=1)
    fig.update_xaxes(title_text="Log10(Revenue)", row=1, col=2)
    fig.update_yaxes(title_text="Frequency", row=1, col=2)

    fig.write_html(
        f"{SAVE_PATH}budget_and_revenue_distributions.html",
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
        title_text=f"Average Budget and Revenue Over Time ({annual_stats['release_year'].min()} - {annual_stats['release_year'].max()})",
        title_x=0.5,
        xaxis=dict(title="Release Year"),
        yaxis=dict(
            title="Average Budget ($)",
            titlefont=dict(color="rgb(102,194,165)"),
            tickfont=dict(color="rgb(102,194,165)"),
            showgrid=True,
            zeroline=True,
        ),
        yaxis2=dict(
            title="Average Revenue ($)",
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
    )

    fig.write_html(
        f"{SAVE_PATH}budget_revenue_over_time.html",
        config={"toImageButtonOptions": {"filename": "budget_revenue_over_time"}},
    )

    # Show the interactive plot
    fig.show()


import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np


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
    plot_data = (
        transformation(data[column].dropna())
        if transformation
        else data[column].dropna()
    )

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
        template="plotly_white",
    )

    # Write HTML file
    fig.write_html(
        f"{SAVE_PATH}roi_distribution.html",
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
        title="Average ROI by Movie Genre (with 90% CI)",
        # center the title
        title_x=0.5,
        xaxis_title="Average Return on Investment (ROI)",
        yaxis_title="Movie Genre",
        template="plotly_white",
        margin=dict(l=100, r=50, t=50, b=50),
        xaxis=dict(gridcolor="rgba(0,0,0,0.1)", zerolinecolor="rgba(0,0,0,0.3)"),
        bargap=0.4,
    )

    # Add a vertical line at x=0
    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="black")

    fig.write_html(
        f"{SAVE_PATH}roi_by_genre.html",
        config={"toImageButtonOptions": {"filename": f"roi_by_genre"}},
    )

    # Show the interactive plot
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
        title="Distribution of Budget per Genre (for Top 20 Genres)",
        labels={"genres_list": "Genre", "log_budget": "Log10(Budget)"},
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Genre",
        yaxis_title="Log10(Budget)",
        xaxis=dict(tickangle=45),
        showlegend=False,
        template="plotly_white",
    )

    # write the plot to an HTML file
    fig.write_html(
        f"{SAVE_PATH}budget_per_genre.html",
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
        title="Budget vs. Revenue-to-Budget Ratio",
        title_x=0.5,
        xaxis=dict(
            title="Inflated Budget (Log Scale)",
            type="log",
            showgrid=True,
            gridcolor="lightgray",
        ),
        yaxis=dict(
            title="Revenue-to-Budget Ratio Logarithmic",
            showgrid=True,
            gridcolor="lightgray",
        ),
        template="plotly_white",
    )

    # write the plot to an HTML file
    fig.write_html(
        f"{SAVE_PATH}revenue_to_budget_ratio.html",
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
            marker_color=px.colors.qualitative.Set2[0],
        )
    )

    # Add Spearman bar
    fig.add_trace(
        go.Bar(
            x=genre_corrs["Spearman"],
            y=genre_corrs.index,
            orientation="h",
            name="Spearman",
            marker_color=px.colors.qualitative.Set2[1],
        )
    )

    # Update layout for better readability
    fig.update_layout(
        title_x=0.5,
        barmode="group",
        title="Correlation between Budget and Revenue per Genre (Log-Log Scale)",
        xaxis_title="Correlation Coefficient",
        yaxis_title="Genre",
        template="simple_white",
        legend_title="Correlation Type",
        height=800,
    )

    # write the plot to an HTML file
    fig.write_html(
        f"{SAVE_PATH}budget_correlation_per_genre.html",
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
        color_continuous_scale="peach",
        title="Movie Budget vs Revenue Distribution",
        labels={"log_budget": "Log10(Budget)", "log_revenue": "Log10(Revenue)"},
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
        xaxis_title="Budget (Log Scale)",
        yaxis_title="Revenue (Log Scale)",
        coloraxis_colorbar=dict(title="Count"),
        template="plotly_white",
        showlegend=True,
        legend=dict(y=1.05),  # Move legend a bit up
        title_x=0.5,
        height=600,
        width=800,
    )

    # write the plot to an HTML file
    fig.write_html(
        f"{SAVE_PATH}budget_vs_revenue_hexbin.html",
        config={"toImageButtonOptions": {"filename": "budget_vs_revenue_hexbin"}},
    )

    fig.show()
