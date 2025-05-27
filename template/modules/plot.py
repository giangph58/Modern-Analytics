from shiny import module, reactive, ui
from shinywidgets import (
    output_widget,
    render_widget,
)
from utils.helper_text import (
    about_text,
    dataset_information,
    missing_note,
    slider_text_plot,
)
from utils.plot_utils import create_figure

from data import plot_data

country_choices = plot_data["Entity"].unique().tolist()


@module.ui
def plot_ui():
    return ui.tags.div(
        ui.tags.div(
            about_text,
            ui.tags.hr(),
            slider_text_plot,
            ui.tags.br(),
            ui.input_slider(
                id="years_value",
                label="Select Year",
                min=2013,
                max=2024,
                value=[2015, 2021],
                sep="",
            ),
            ui.input_selectize(
                id="country_select",
                label="Select Countries:",
                choices=country_choices,
                selected=country_choices[0],
                multiple=True,
            ),
            ui.tags.hr(),
            dataset_information,
            ui.tags.hr(),
            missing_note,
            class_="main-sidebar card-style",
        ),
        ui.tags.div(
            output_widget("hly_plot"),
            ui.tags.hr(),
            output_widget("gdp_plot"),
            class_="main-main card-style",
        ),
        class_="main-layout",
    )


@module.server
def plot_server(input, output, session):
    @reactive.Calc
    def data():
        return plot_data

    @reactive.Calc
    def fig_one():
        filtered_data = data()
        # Filter for HLY at the figure level instead
        hly_data_subset = filtered_data[filtered_data["HealthyLifeYears"].notna()]

        return create_figure(
            data=hly_data_subset,
            year_range=input.years_value(),
            country=input.country_select(),
            y_from="HealthyLifeYears",
            title="Healthy Life Years",
            labels={"Year": "Year", "HealthyLifeYears": "Healthy Life Years"},
        )

    @reactive.Calc
    def fig_two():
        return create_figure(
            data=data(),
            year_range=input.years_value(),
            country=input.country_select(),
            y_from="GDP",
            title="Gross Domestic Product",
            labels={
                "Year": "Year",
                "GDP": "GDP",
            },
        )

    # @output(suspend_when_hidden=False)
    @render_widget
    def hly_plot():
        return fig_one()

    # @output(suspend_when_hidden=False)
    @render_widget
    def gdp_plot():
        return fig_two()
