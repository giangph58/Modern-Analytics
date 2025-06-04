from shiny import ui, render, reactive
from utils.graph_utils import load_health_data, build_country_network, create_network_plot

def graph_ui(id):
    """UI for the network graph visualization module"""
    return ui.page_fluid(
        ui.div(
            ui.h2("EU Health Research Collaboration Network"),
            ui.p(
                """This network visualization shows collaborative relationships between European countries 
                in health research projects funded by Horizon Europe. The geographical layout allows you to 
                see regional patterns in research collaborations.""",
                class_="module-description"
            ),
            ui.div(
                ui.input_slider(
                    id="min_collaborations",
                    label="Minimum collaborations threshold:",
                    min=1,
                    max=20,
                    value=5,
                    step=1
                ),
                ui.input_checkbox(
                    id="show_labels",
                    label="Show country labels",
                    value=True
                ),
                class_="controls-row"
            ),
            ui.output_plot("network_plot", height="800px", width="100%"),
            ui.div(
                ui.p(
                    """Larger nodes represent countries with more collaborative connections. 
                    Node color indicates the degree centrality (number of partner countries), 
                    and edge width corresponds to the number of joint projects between countries."""
                ),
                class_="plot-explanation"
            ),
            class_="network-container card-style"
        )
    )

def graph_server(id):
    """Server function for network graph visualization"""
    
    # Load data once when the module initializes
    health_orgs = load_health_data()
    
    @reactive.Calc
    def generate_network():
        """Build the network based on current settings"""
        min_weight = input.min_collaborations()
        G, _ = build_country_network(health_orgs, min_weight=min_weight)
        return G
    
    @render.plot
    def network_plot():
        """Render the network visualization"""
        G = generate_network()
        show_labels = input.show_labels()
        fig = create_network_plot(G, show_labels=show_labels)
        return fig