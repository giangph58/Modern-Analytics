from shiny import module, reactive, ui
from shinywidgets import (
    output_widget,
    render_widget,
)
from utils.helper_text import (
    about_text,
    dataset_information,
    missing_note
)
from utils.topic_utils import create_topic_trend, create_topic_total_funding, create_topic_avg_funding, create_topic_total_publication, create_topic_avg_publication, create_static_topic_map

from data import topic_data
import os

topic_choices = topic_data["topic_label"].unique().tolist()


@module.ui
def topic_ui():
    return ui.tags.div(
        ui.tags.div(
            about_text,
            ui.tags.hr(),
            ui.h4("Topic Filter"),
            ui.input_selectize(
                id="topic_select",
                label="Select Topics:",
                choices=topic_choices,
                multiple=True,
                selected=topic_choices
            ),
            ui.tags.br(),
            ui.tags.hr(),
            dataset_information,
            ui.tags.hr(),
            missing_note,
            class_="main-sidebar card-style",
        ),
        ui.tags.div(
            ui.tags.h4("Topic Document Datamap"),
            output_widget("topic_static_map"),
            ui.tags.hr(),
            ui.tags.h4("Topic Trend over time"),
            output_widget("topic_trend_plot"),
            ui.tags.hr(),
            ui.tags.h4("Total Funding by Topic"),
            output_widget("topic_total_funding_plot"),
            ui.tags.hr(),
            ui.tags.h4("Average Funding per Project by Topic"),
            output_widget("topic_avg_funding_plot"),
            ui.tags.hr(),
            ui.tags.h4("Total Publications by Topic"),
            output_widget("topic_total_publication_plot"),
            ui.tags.hr(),
            ui.tags.h4("Average Publications per Project by Topic"),
            output_widget("topic_avg_publication_plot"),
            class_="main-main card-style",
        ),
        class_="main-layout",
    )


@module.server
def topic_server(input, output, session):
    @reactive.Calc
    def data():
        return topic_data
    
    @reactive.Calc
    def fig_static_topic_map():
        app_dir = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(app_dir, "www", "static", "img", "doc_map.png")
        return create_static_topic_map(image_path)
    
    @reactive.Calc
    def fig_one():
        return create_topic_trend(
            data=data(),
            topic=input.topic_select(),
            title="",
            labels={"time_period": "Year", "count": "Project Count"},
        )
    
    @reactive.Calc
    def fig_two():
        return create_topic_total_funding(
            data=data(),
            topic=input.topic_select(),
            title="",
            labels={"ecMaxContribution": "Total EC Contribution", "topic": "Topic"}
        )

    @reactive.Calc
    def fig_three():
        return create_topic_avg_funding(
            data=data(),
            topic=input.topic_select(),
            title="",
            labels={"ecMaxContribution": "Total EC Contribution", "topic": "Topic"}
        )

    @reactive.Calc
    def fig_four():
        return create_topic_total_publication(
            data=data(),
            topic=input.topic_select(),
            title="",
            labels={"publication_count": "Total Publications", "topic": "Topic",}
        )
    
    @reactive.Calc
    def fig_five():
        topic_funding_data = data()

        return create_topic_avg_publication(
            data=data(),
            topic=input.topic_select(),
            title="",
            labels={"publication_count": "Total Publications", "topic": "Topic",}
        )

    @render_widget
    def topic_static_map():
        return fig_static_topic_map()

    # @render_widget
    # def topic_kwords_plot():
    #     return fig_topic_kwords()

    @render_widget
    def topic_trend_plot():
        return fig_one()

    @render_widget
    def topic_total_funding_plot():
        return fig_two()

    @render_widget
    def topic_avg_funding_plot():
        return fig_three()


    @render_widget
    def topic_total_publication_plot():
        return fig_four()
    
    @render_widget
    def topic_avg_publication_plot():
        return fig_five()
    
    