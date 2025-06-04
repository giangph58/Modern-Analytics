import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
from itertools import combinations
from collections import Counter

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

# Country code to name mapping
country_names = {
    'BE': 'Belgium', 'BG': 'Bulgaria', 'CZ': 'Czechia', 'DK': 'Denmark', 'DE': 'Germany',
    'EE': 'Estonia', 'IE': 'Ireland', 'GR': 'Greece', 'ES': 'Spain', 'FR': 'France',
    'HR': 'Croatia', 'IT': 'Italy', 'CY': 'Cyprus', 'LV': 'Latvia', 'LT': 'Lithuania',
    'LU': 'Luxembourg', 'HU': 'Hungary', 'MT': 'Malta', 'NL': 'Netherlands', 'AT': 'Austria',
    'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'SI': 'Slovenia', 'SK': 'Slovakia',
    'FI': 'Finland', 'SE': 'Sweden', 'IS': 'Iceland', 'LI': 'Liechtenstein', 'NO': 'Norway',
    'CH': 'Switzerland', 'GB': 'United Kingdom', 'BA': 'Bosnia and Herzegovina',
    'ME': 'Montenegro', 'MK': 'North Macedonia', 'AL': 'Albania', 'RS': 'Serbia',
    'TR': 'Türkiye', 'UA': 'Ukraine', 'NULL': 'Kosovo'
}

def load_health_data():
    """
    Load and prepare health project organization data
    """
    # Load datasets
    health_df = pd.read_csv("data/interim/health.csv")
    orgs = pd.read_excel("data/raw/organization.xlsx")
    
    # Define European countries
    european_countries = [
        'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR',
        'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK',
        'SI', 'ES', 'SE', 'NO', 'IS', 'LI', 'CH', 'GB', 'BA', 'ME', 'MK', 'AL',
        'RS', 'TR', 'UA', 'NULL'  # 'NULL' for Kosovo
    ]
    
    # Get list of health-related project IDs
    health_ids = health_df['projectID'].unique()
    
    # Select only participants in health projects
    health_orgs = orgs[orgs['projectID'].isin(health_ids)]
    
    # Filter for European countries and add country names
    health_orgs = health_orgs[health_orgs['country'].isin(european_countries)]
    health_orgs['country_name'] = health_orgs['country'].map(country_names)
    
    return health_orgs

def build_country_network(health_orgs, min_weight=5):
    """
    Build a network graph of country collaborations based on project data
    """
    country_edges = []

    # Create edges between countries collaborating on the same project
    for pid, group in health_orgs.groupby('projectID'):
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