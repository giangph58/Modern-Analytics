from utils.helper_text import (
    about_graph,
    dataset_information,
    missing_note
)

from shiny import ui, render, reactive, module
from shinywidgets import (
    output_widget,
    render_widget,
)
from utils.graph_utils import build_country_network, create_network_plot, create_trendline_plot
from data import orgs_data, orgs_pub_data
import pandas as pd

@module.ui
def graph_ui():
    return ui.tags.div(
        ui.tags.div(
            about_graph,
            ui.tags.hr(),
            dataset_information,
            ui.tags.hr(),
            missing_note,
            class_="main-sidebar card-style",
        ),
        ui.tags.div(
            ui.tags.h4("EU Health Research Collaboration Network"),
            ui.output_plot("network_plot", height="1000px", width="100%"),
            ui.tags.hr(),
            ui.tags.div(
                ui.tags.h4("Top Country Collaborations"),
                ui.input_numeric("top_country_n", "Number of top country pairs to display:", value=10, min=5, max=30),
                ui.output_table("country_table"),
                class_="table-container"
            ),
            ui.tags.hr(),
            ui.tags.div(
                ui.tags.h4("Top Project Coordinators"),
                ui.input_numeric("top_n", "Number of top coordinators to display:", value=10, min=5, max=50),
                ui.output_table("coordinators_table"),
                class_="table-container"
            ),
            ui.tags.h4("Coordination vs Publications Analysis"),
            output_widget("orgs_pub_plot"),
            ui.tags.hr(),
            class_="main-main card-style",
        ),
        class_="main-layout",
    )

@module.server
def graph_server(input, output, session):
    """Server function for network graph visualization"""
    
    @reactive.Calc
    def data():
        return orgs_data
    
    @reactive.Calc
    def pub_data():
        return orgs_pub_data
    
    @reactive.Calc
    def generate_network():
        """Build the network based on current settings"""
        min_weight = 5
        G, _ = build_country_network(data(), min_weight=min_weight)
        return G
    
    @render.plot
    def network_plot():
        """Render the network visualization"""
        G = generate_network()
        fig = create_network_plot(G)
        return fig
    
    @reactive.Calc
    def country_collaboration_data():
        """Generate data for country collaboration table"""
        from itertools import combinations
        from collections import Counter
        
        health_orgs = data()
        country_edges = []

        for pid, group in health_orgs.groupby('projectID'):
            countries = group['country_name'].dropna().unique()
            if len(countries) >= 2:
                for pair in combinations(sorted(countries), 2):
                    country_edges.append(pair)

        edge_counts = Counter(country_edges)

        edge_df = pd.DataFrame(edge_counts.items(), columns=['Country Pair', 'Num Projects'])
        edge_df = edge_df.sort_values(by='Num Projects', ascending=False)

        edge_df[['Country A', 'Country B']] = pd.DataFrame(edge_df['Country Pair'].tolist(), index=edge_df.index)
        edge_df.drop(columns='Country Pair', inplace=True)
        
        # Reorder columns: Country A, Country B, Number of Projects
        edge_df = edge_df[['Country A', 'Country B', 'Num Projects']]
        edge_df.columns = ['Country A', 'Country B', 'Number of Projects']  # Rename for consistency
        
        # Get top N country pairs
        top_country_n = input.top_country_n()
        return edge_df.head(top_country_n)
        

    @reactive.Calc
    def coordination_analysis_data():
        """Generate data for coordination vs publications analysis"""
        # Filter for coordinator records from publication data
        health_coordinators = pub_data()[pub_data()['role'].str.lower() == 'coordinator']
        
        # Frequency of coordination
        coord_freq = health_coordinators['name'].value_counts().reset_index()
        coord_freq.columns = ['name', 'coord_count']
        
        # Publication counts merged
        pubs_per_org = health_coordinators.groupby('name')['publicationCount'].sum().reset_index()
        
        # Merge both
        combined = pd.merge(coord_freq, pubs_per_org, on='name')
        combined.columns = ['Institution', 'Coordinated Projects', 'Total Publications']
        
        return combined
    
    @reactive.Calc
    def trendline_plot():
        """Render the coordination vs publications interactive trendline plot"""
        combined = coordination_analysis_data()
        
        return create_trendline_plot(
            data=combined,
            x_col='Coordinated Projects',
            y_col='Total Publications',
            text_col='Institution',
            title="Do Coordinators with More Projects Publish More?",
            labels={
                'Coordinated Projects': 'Number of Coordinated Projects',
                'Total Publications': 'Total Publications'
            }
        )
        
    @reactive.Calc
    def top_coordinators_data():
        """Generate data for top coordinators table"""
        # Filter for coordinator records
        health_coordinators = data()[data()['role'].str.lower() == 'coordinator']
        
        # Count projects per coordinator and get top N
        top_n = input.top_n()
        coordinator_counts = (
            health_coordinators
                .groupby(['name', 'country_name'])
                .size()
                .reset_index(name='num_coordinated_projects')
                .sort_values(by='num_coordinated_projects', ascending=False)
        )
                                                 
        coordinator_counts.columns = ['Organization', "Country", "Number of Coordinated Projects"]
        
        # Get top N coordinators
        return coordinator_counts.head(top_n)
    
    @render.table
    def country_table():
        """Render the top country collaborations table"""
        return country_collaboration_data()


    @render.table
    def coordinators_table():
        """Render the top coordinators table"""
        return top_coordinators_data()
    
    @render_widget
    def orgs_pub_plot():
        return trendline_plot()