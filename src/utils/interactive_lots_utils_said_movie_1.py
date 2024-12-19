import plotly.graph_objects as go


SAVE_PATH = "../c1n3mada-datastory/assets/plots/echo/"


def plot_rating_revenue_correlation(df_rating):
    # Calculate correlation matrix
    corr_matrix = df_rating[["averageRating", "inflated_revenue", "numVotes"]].corr()

    # Create the heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale="RdBu",  # Diverging color scale for positive and negative correlations
            zmin=-1,
            zmax=1,  # Set min and max correlation values for consistent color scaling
            text=corr_matrix.values.round(
                2
            ),  # Display rounded correlation values within cells
            texttemplate="%{text}",
            hovertemplate="<b>x: %{x}</b><br><b>y: %{y}</b><br><b>Correlation: %{z:.2f}</b>",  # Improved hover information
            name="Correlation Score",
        )
    )

    fig.update_layout(
        title_text="Correlation Matrix",
        xaxis_title="Features",
        yaxis_title="Features",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="black",
        title_x=0.5,  # Center the title
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )

    fig.write_html(
        f"{SAVE_PATH}rating_revenue_correlation.html",
        config={"toImageButtonOptions": {"filename": "rating_revenue_correlation"}},
    )

    fig.show()
