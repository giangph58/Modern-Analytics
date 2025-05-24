import shiny
from shiny import App, ui, render
from shiny.ui import layout_sidebar, sidebar
import numpy as np
import matplotlib.pyplot as plt


app_ui = ui.page_fluid(
    ui.h1("Third app ..."),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_numeric("n", "Sample size", 10),
            ui.input_text("title", "Title of ...", "Fancy Boxplot ..."),
            ui.input_radio_buttons("color", "Choose ...", ["Blue", "Green"], selected="Green")
        ),
        ui.output_plot("box")
    )
)


def server(input, output, session):
    @render.plot
    def box():
        data = np.random.rand(input.n())
        fig, ax = plt.subplots()
        ax.boxplot(data, patch_artist=True, boxprops=dict(facecolor=input.color().lower()))
        ax.set_title(input.title())
        ax.set_xlabel("Sample data")
        return fig


app = App(app_ui, server)

