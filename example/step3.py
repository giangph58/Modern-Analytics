import shiny
from shiny import App, ui, render
from shiny.ui import layout_sidebar, sidebar

app_ui = ui.page_fluid(
    ui.h1("First app ..."),
    ui.layout_sidebar(
        ui.sidebar("Sidebar panel ...", position="right"),
        ui.div("Main panel ...")
    )
)


def server(input, output, session):
    pass


app = App(app_ui, server)

