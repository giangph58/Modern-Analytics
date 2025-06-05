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
from utils.plot_utils import create_funds_bar_chart, create_scatter_plot

from data import plot_data

country_choices = plot_data["country_name"].unique().tolist()


@module.ui
def plot_ui():
    return ui.tags.div(
        ui.tags.div(
            about_text,
            ui.tags.hr(),
            slider_text_plot,
            ui.tags.br(),
            ui.input_selectize(
                id="country_select",
                label="Select Countries:",
                choices=country_choices,
                selected=country_choices,
                multiple=True,
            ),
            ui.tags.hr(),
            dataset_information,
            ui.tags.hr(),
            missing_note,
            class_="main-sidebar card-style",
        ),
        ui.tags.div(
            ui.tags.h4("Total Funding for Health by Country"),
            output_widget("funds_plot"),
            ui.tags.hr(),
            ui.tags.h4("Total Funding for Health vs GDP per capita by Country"),
            output_widget("funds_gdp_plot"),
            ui.tags.hr(),
            ui.tags.h4("Total Funding for Health vs Healthy Life Years by Country"),
            output_widget("funds_hly_plot"),
            ui.tags.hr(),
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
        return create_funds_bar_chart(
            data=data(),
            country=input.country_select(),
            y_from="TotalFundsPerCountry",
            title="",
            labels={"TotalFundsPerCountry": "Total Funds (€)"},
        )

    @reactive.Calc
    def funding_vs_gdp_plot():
        return create_scatter_plot(
            data=data(),
            country=input.country_select(),
            x_col="TotalFundsPerCountry",
            y_col="GDPM2124",
            text_col="country_name",
            title="",
            labels={
                "TotalFunds": "Total Funding (EUR)",
                "GDPM2124": "Average GDP 2021–2024 (EUR)",
                "country_name": "Country"
            }
        )

    @reactive.Calc
    def funding_vs_hly_plot():
        return create_scatter_plot(
            data=data(),
            country=input.country_select(),
            x_col="TotalFundsPerCountry",
            y_col="HLYM2122",
            text_col="country_name",
            title="",
            labels={
                "TotalFunds": "Total Funding (EUR)",
                "HLYM2122": "Average HLY 2021–2022 (Years)",
                "country_name": "Country"
            }
        )
    
    # @reactive.Calc
    # def fig_two():
    #     filtered_data = data()
    #     # Filter for HLY at the figure level instead
    #     hly_data_subset = filtered_data[filtered_data["HealthyLifeYears"].notna()]

    #     return create_figure(
    #         data=hly_data_subset,
    #         year_range=input.years_value(),
    #         country=input.country_select(),
    #         y_from="HealthyLifeYears",
    #         title="",
    #         labels={"Year": "Year", "HealthyLifeYears": "Healthy Life Years (years)"},
    #     )

    # @reactive.Calc
    # def fig_three():
    #     return create_figure(
    #         data=data(),
    #         year_range=input.years_value(),
    #         country=input.country_select(),
    #         y_from="GDP",
    #         title="",
    #         labels={
    #             "Year": "Year",
    #             "GDP": "GDP per capita (€)",
    #         },
    #     )

    @render_widget
    def funds_plot():
        return fig_one()

    @render_widget
    def funds_gdp_plot():
        return funding_vs_gdp_plot()

    @render_widget
    def funds_hly_plot():
        return funding_vs_hly_plot()

