from utils.helper_text import (
    about_text,
    dataset_information,
    missing_note,
    slider_text_plot,
)

from shiny import ui, render, reactive, module
from utils.graph_utils import build_country_network, create_network_plot
from data import orgs_data, orgs_pub_data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@module.ui
def graph_ui():
    return ui.tags.div(
        ui.tags.div(
            about_text,
            ui.tags.hr(),
            slider_text_plot,
            ui.tags.br(),
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
                ui.tags.h4("Coordination vs Publications Analysis"),
                ui.output_plot("trendline_plot", height="500px", width="100%"),
                class_="plot-container"
            ),
            ui.tags.hr(),
            ui.tags.div(
                ui.tags.h4("Top Project Coordinators"),
                ui.input_numeric("top_n", "Number of top coordinators to display:", value=10, min=5, max=50),
                ui.output_table("coordinators_table"),
                class_="table-container"
            ),
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
    
    @render.plot
    def trendline_plot():
        """Render the coordination vs publications trendline plot"""
        combined = coordination_analysis_data()
        
        plt.figure(figsize=(10, 6))
        sns.regplot(
            data=combined,
            x='Coordinated Projects',
            y='Total Publications',
            scatter=True,
            color='red'
        )
        
        plt.title("Do Coordinators with More Projects Publish More?")
        plt.xlabel("Number of Coordinated Projects")
        plt.ylabel("Total Publications")
        plt.grid(True)
        plt.tight_layout()
        
        return plt.gcf()
        
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
    def coordinators_table():
        """Render the top coordinators table"""
        return top_coordinators_data()