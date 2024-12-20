import plotly.graph_objects as go
import plotly.express as px

SAVE_PATH_SHADES = "../c1n3mada-datastory/assets/plots/shades/"


def create_interactive_correlation_shades(
    df_correlation,
    title="Correlation between Number of Movies and Average Box Office Revenue per Genre over Time",
):
    genre_corrs_sorted = df_correlation.sort_values("Pearson", ascending=True)
    x_pearson = genre_corrs_sorted["Pearson"]
    x_spearman = genre_corrs_sorted["Spearman"]
    y = genre_corrs_sorted.index

    # set 2 palette colors
    possible_colors = px.colors.qualitative.Set2

    # figure
    fig = go.Figure()

    # add Pearson bars
    fig.add_trace(
        go.Bar(
            x=x_pearson,
            y=y,
            orientation="h",
            name="Pearson",
            marker=dict(color=possible_colors[0]),
            text=[f"{val:.3f}" for val in x_pearson],
            textposition="outside",
        )
    )

    # add Spearman bars
    fig.add_trace(
        go.Bar(
            x=x_spearman,
            y=y,
            orientation="h",
            name="Spearman",
            marker=dict(color=possible_colors[1]),
            text=[f"{val:.3f}" for val in x_spearman],
            textposition="outside",
        )
    )
    fig.update_layout(
        # title=title,
        xaxis=dict(title="Correlation Coefficient", gridcolor="lightgray"),
        yaxis=dict(title="Genre", automargin=True),
        barmode="group",
        legend=dict(title="Correlation Type"),
        margin=dict(l=100, r=40, t=80, b=40),
        title_x=0.5,
        title_font=dict(family="Arial"),
        title=dict(text=title, pad=dict(t=10, b=0)),
        template="plotly_white",
    )

    fig.write_html(
        f"{SAVE_PATH_SHADES}correlation_shades.html",
        config={"toImageButtonOptions": {"filename": "correlation_shades"}},
    )
    fig.show()
