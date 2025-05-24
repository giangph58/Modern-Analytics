import shiny
from shiny import App, ui, render
from shiny.ui import layout_sidebar, sidebar

app_ui = ui.page_fluid()

def server(input, output, session):
    pass


app = App(app_ui, server)
