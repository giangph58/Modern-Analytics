from pathlib import Path

from modules import plot, graph, topic
from shiny import App, Session, reactive, ui
from utils.helper_text import info_modal

page_dependencies = ui.tags.head(
    ui.tags.link(rel="stylesheet", type="text/css", href="layout.css"),
    ui.tags.link(rel="stylesheet", type="text/css", href="style.css"),
    ui.tags.script(src="index.js"),
    ui.tags.meta(name="description", content="Climate Health Dashboard"),
    ui.tags.meta(name="theme-color", content="#000000"),
    ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
)

# top navbar
page_header = ui.tags.div(
    ui.tags.div(
        ui.tags.a(
            ui.tags.img(src="static/img/appsilon-logo.png", height="50px"),
            href="https://demo.appsilon.com/",
        ),
        id="logo-top",
        class_="navigation-logo",
    ),
    ui.tags.div(
        ui.tags.div(
            ui.input_action_button(
                id="tab_funding",
                label="Funding and Impact",
                class_="navbar-button",
            ),
            id="div-navbar-funding",
        ),
        ui.tags.div(
            ui.input_action_button(
                id="tab_graph",
                label="Collaborations",
                class_="navbar-button",
            ),
            id="div-navbar-graph",
        ),
        ui.tags.div(
            ui.input_action_button(
                id="tab_topic",
                label="Topics",
                class_="navbar-button",
            ),
            id="div-navbar-topic",
        ),
        id="div-navbar-tabs",
        class_="navigation-menu",
    ),
    ui.tags.div(
        ui.input_action_button(
            id="info_icon",
            label=None,
            icon=ui.tags.i(class_="glyphicon glyphicon-info-sign"),
            class_="navbar-info",
        ),
        class_="navigation-info",
    ),
    id="div-navbar",
    class_="navbar-top page-header card-style",
)

plot_ui = ui.tags.div(
    plot.plot_ui("plot"),
    id="plot-container",
    class_="page-main",
)

graph_ui = ui.tags.div(
    graph.graph_ui("graph"),
    id="graph-container",
    class_="page-main",
)

topic_ui = ui.tags.div(
    topic.topic_ui("topic"),
    id="topic-container", 
    class_="page-main",
)


page_layout = ui.tags.div(page_header, plot_ui, graph_ui, topic_ui, class_="page-layout")

app_ui = ui.page_fluid(
    page_dependencies,
    page_layout,
    title="Horizon Europe Health Dashboard",
)


def server(input, output, session: Session):
    info_modal()

    @reactive.Effect
    @reactive.event(input.info_icon)
    def _():
        info_modal()

    plot.plot_server("plot")
    graph.graph_server("graph")
    topic.topic_server("topic")

    @reactive.Effect
    @reactive.event(input.tab_funding)
    async def _():
        await session.send_custom_message("toggleActiveTab", {"activeTab": "plot"})

    @reactive.Effect
    @reactive.event(input.tab_graph)
    async def _():
        await session.send_custom_message("toggleActiveTab", {"activeTab": "graph"})


    @reactive.Effect
    @reactive.event(input.tab_topic)
    async def _():
        await session.send_custom_message("toggleActiveTab", {"activeTab": "topic"})


www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)
