import plotly.graph_objects as go

SAVE_PATH_SHADES = "../c1n3mada-datastory/assets/plots/shades/"

def create_interactive_correlation_shades(df_correlation, title="Correlation between IMDb Ratings and Revenue by Genre"):
    genre_corrs_sorted = df_correlation.sort_values("Pearson", ascending=True)
    x_pearson = genre_corrs_sorted["Pearson"]
    x_spearman = genre_corrs_sorted["Spearman"]
    y = genre_corrs_sorted.index

    # figure
    fig = go.Figure()

    # add Pearson bars
    fig.add_trace(
        go.Bar(
            x=x_pearson,
            y=y,
            orientation='h',
            name='Pearson',
            marker=dict(color='#2ecc71'),
            text=[f"{val:.3f}" for val in x_pearson],
            textposition="outside",
        )
    )

    # add Spearman bars
    fig.add_trace(
        go.Bar(
            x=x_spearman,
            y=y,
            orientation='h',
            name='Spearman',
            marker=dict(color='#3498db'),
            text=[f"{val:.3f}" for val in x_spearman],
            textposition="outside",
        )
    )
    fig.update_layout(
        title=title,
        title_font=dict(size=16, color="black"),
        xaxis=dict(title="Correlation Coefficient", gridcolor="lightgray"),
        yaxis=dict(title="Genre", automargin=True),
        barmode="group",
        legend=dict(title="Correlation Type"),
        margin=dict(l=100, r=40, t=80, b=40),
        template="plotly_white",
    )

    fig.write_html(f"{SAVE_PATH_SHADES}correlation_shades.html", config={"toImageButtonOptions": {"filename": "correlation_shades"}})
    fig.show()