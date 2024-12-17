import numpy as np
import plotly.express as px

# Interactive plots for Shades 
def create_interactive_revenue_trends_over_time_heatmap(mean_revenue_pivot):
    mean_revenue_pivot = mean_revenue_pivot.replace(0, np.nan)
    fig = px.imshow(
        mean_revenue_pivot.T, 
        labels=dict(x="Release Year", y="Genre", color="Average Revenue"),
        title="Interactive Heatmap: Average Box Office Revenue per Genre Over Time",
        color_continuous_scale="matter",  
        aspect="auto",  
    )

    fig.update_layout(
        width=1000, height=800,  
        xaxis=dict(tickangle=45),  
    )
    fig.write_html("interactive_plots/shades/revenue_trends_over_time_heatmap.html")
    fig.show()