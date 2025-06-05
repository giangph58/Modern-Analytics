import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from itertools import combinations
from collections import Counter
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go
import numpy as np



# Geographic positions for European countries
geo_pos = {
    'Portugal': (1, 3),
    'Spain': (2, 3),
    'France': (3, 4),
    'Germany': (5, 5),
    'Italy': (5, 3),
    'Belgium': (4, 5),
    'Netherlands': (4.5, 5.5),
    'Luxembourg': (4.2, 4.7),
    'Ireland': (1.5, 6),
    'United Kingdom': (2.5, 6),
    'Denmark': (6, 6),
    'Sweden': (7, 8),
    'Finland': (8, 9),
    'Norway': (6, 9),
    'Poland': (7, 5),
    'Czechia': (6, 4.5),
    'Austria': (6, 4),
    'Switzerland': (5, 4.5),
    'Slovakia': (7, 4),
    'Hungary': (7.5, 3.5),
    'Slovenia': (6.5, 3),
    'Croatia': (7, 3),
    'Romania': (8.5, 3.5),
    'Bulgaria': (9, 3),
    'Greece': (9.5, 2.5),
    'Cyprus': (11, 1),
    'Estonia': (8, 7),
    'Latvia': (8, 6),
    'Lithuania': (8, 5.5),
    'Malta': (6, 1),
    'Serbia': (8, 2.5),
    'Albania': (8.5, 2),
    'North Macedonia': (8.5, 1.5),
    'Montenegro': (8, 1.7),
    'Bosnia and Herzegovina': (7.5, 2),
    'Türkiye': (10, 1),
    'Ukraine': (10, 4),
    'Iceland': (0, 9)
}


def build_country_network(data: DataFrame, min_weight=5):
    """
    Build a network graph of country collaborations based on project data
    """
    country_edges = []

    # Create edges between countries collaborating on the same project
    for pid, group in data.groupby('projectID'):
        countries = group['country_name'].dropna().unique()
        if len(countries) >= 2:
            for pair in combinations(sorted(countries), 2):
                country_edges.append(pair)

    edge_counts = Counter(country_edges)
    
    # Create graph with minimum weight threshold
    G = nx.Graph()
    for (c1, c2), weight in edge_counts.items():
        if weight >= min_weight:
            G.add_edge(c1, c2, weight=weight)
            
    return G, edge_counts

def create_network_plot(G, show_labels=True, figsize=(14, 12)):
    """
    Create network visualization with geographic positioning
    """
    # Calculate node properties
    node_degrees = dict(G.degree())
    node_sizes = [node_degrees[node] * 100 for node in G.nodes()]
    
    # Color mapping based on node degrees
    norm = colors.Normalize(vmin=min(node_degrees.values()), vmax=max(node_degrees.values()))
    cmap = plt.colormaps['viridis']
    node_colors = [cmap(norm(node_degrees[node])) for node in G.nodes()]
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Draw nodes
    nodes = nx.draw_networkx_nodes(
        G, geo_pos, ax=ax,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors='black'
    )
    
    # Draw edges
    nx.draw_networkx_edges(
        G, geo_pos, ax=ax,
        width=[G[u][v]['weight'] * 0.3 for u, v in G.edges()],
        edge_color='gray',
        alpha=0.6
    )
    
    # Draw labels if requested
    if show_labels:
        nx.draw_networkx_labels(G, geo_pos, ax=ax, font_size=9, font_weight='bold')
    
    # Title and colorbar
    ax.set_title("EU Health Collaborations by Country (Node Color = Degree)")
    ax.axis('off')
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])  # needed for colorbar to render properly
    cbar = fig.colorbar(sm, ax=ax, shrink=0.8)
    cbar.set_label('Number of Collaborating Countries')
    
    plt.tight_layout()
    return fig


# Add this function to graph_utils.py after the existing functions


def create_trendline_plot(
    data: DataFrame,
    x_col: str,
    y_col: str,
    text_col: str,
    title: str,
    labels: dict,
) -> go.Figure:
    """
    Create an interactive scatter plot with trendline and 95% CI (consistent with seaborn regplot)
    """
    # Remove rows with missing data
    plot_data = data.dropna(subset=[x_col, y_col])
    
    if plot_data.empty:
        fig = go.Figure()
        fig.update_layout(title="No data available")
        return fig
    
    # Create interactive scatter plot without text annotations
    fig = px.scatter(
        plot_data,
        x=x_col,
        y=y_col,
        hover_name=text_col,  # Show institution names only on hover
        labels=labels,
        color_discrete_sequence=['red'],  # Changed to red to match regplot
    )
    
    # Add regression line with 95% CI if we have enough data points
    if len(plot_data) > 2:  # Need at least 3 points for proper CI calculation
        x_vals = plot_data[x_col].values
        y_vals = plot_data[y_col].values
        
        # Linear regression using statsmodels for proper CI calculation
        import statsmodels.api as sm
        
        # Add constant for intercept
        X = sm.add_constant(x_vals)
        model = sm.OLS(y_vals, X).fit()
        
        # Generate prediction points
        x_range = np.linspace(x_vals.min(), x_vals.max(), 100)
        X_pred = sm.add_constant(x_range)
        
        # Get predictions with confidence intervals
        predictions = model.get_prediction(X_pred)
        pred_summary = predictions.summary_frame(alpha=0.05)  # 95% CI
        
        # Add regression line (red color to match seaborn)
        fig.add_trace(go.Scatter(
            x=x_range,
            y=pred_summary['mean'],
            mode='lines',
            name='Linear Regression',
            line=dict(color='red', width=2),
            hovertemplate="Linear Regression<extra></extra>"
        ))
        
        # Add 95% confidence interval band (light red to match seaborn style)
        fig.add_trace(go.Scatter(
            x=np.concatenate([x_range, x_range[::-1]]),
            y=np.concatenate([pred_summary['mean_ci_upper'], pred_summary['mean_ci_lower'][::-1]]),
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.2)',  # Light red
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name="95% CI",
            showlegend=True  # Show in legend like seaborn
        ))
        
        # Calculate R-squared
        r_squared = model.rsquared
        
        # Add R-squared as annotation
        fig.add_annotation(
            x=0.05,
            y=0.95,
            xref="paper",
            yref="paper",
            text=f"R² = {r_squared:.3f}",
            showarrow=False,
            font=dict(size=14, color="black"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1
        )
    
    # Font configs
    xaxis_font_size = 16
    yaxis_font_size = 16
    axis_title_size = 20
    
    # Update layout
    fig.update_traces(
        marker=dict(size=8, opacity=0.7, color='red'),  # Red markers to match
        selector=dict(mode="markers")
    )
    
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title=None,  # Remove title
        xaxis=dict(
            title=labels.get(x_col, x_col),
            title_font=dict(size=axis_title_size),
            tickfont=dict(size=xaxis_font_size),
            showgrid=True,
            gridcolor="lightgrey",
            linecolor="black",
            mirror=True
        ),
        yaxis=dict(
            title=labels.get(y_col, y_col),
            title_font=dict(size=axis_title_size),
            tickfont=dict(size=yaxis_font_size),
            showgrid=True,
            gridcolor="lightgrey",
            linecolor="black",
            mirror=True
        ),
        legend=dict(
            font=dict(size=16)
        ),
        hovermode="closest",
        height=600,  # Increased height
        width=1200,  # Increased width
        margin=dict(l=100, r=50, t=50, b=70)
    )
    
    return fig

