import shiny
from shiny import App, ui, render
from shiny.ui import layout_sidebar, sidebar
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


iris = sns.load_dataset("iris")

app_ui = ui.page_fluid(
    ui.h1("Fourth app ..."),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider("sepal_length", "Sepal.Length:", min=4.3, max=7.9, value=5.8, step=0.1),
            ui.input_slider("sepal_width", "Sepal.Width:", min=2.0, max=4.4, value=3.0, step=0.1),
            ui.input_slider("petal_length", "Petal.Length:", min=1.0, max=6.9, value=(1.6, 5.1)),
            ui.input_slider("petal_width", "Petal.Width:", min=1.0, max=2.5, value=1.3, step=0.3)
        ),
    )
)

def server(input, output, session):
    pass


app = App(app_ui, server)
