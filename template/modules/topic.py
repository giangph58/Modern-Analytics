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
from utils.topic_utils import create_topic_trend, create_topic_total_funding, create_topic_avg_funding, create_topic_total_publication, create_topic_avg_publication, create_topic_kwords, create_static_topic_map

from data import load_topic_data, load_topic_model, load_2comp_embeddings, load_5comp_embeddings, load_titles
import plotly.graph_objects as go
import os


@module.ui
def topic_ui():
    topic_options = {i: f"Topic {i}" for i in range(23)}

    return ui.tags.div(
        ui.tags.div(
            about_text,
            ui.tags.hr(),
            # slider_text_plot,
            ui.h4("Topic Filter"),
            ui.input_selectize(
                id="selected_topics",
                label="Select topicse:",
                choices=topic_options,
                multiple=True,
                selected=list(range(23))  # Default to all topics
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
            ui.tags.h4("Topic Key Words"),
            output_widget("topic_kwords_plot"),
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
        return load_topic_data()

    @reactive.Calc
    def embeddings_2comp():
        return load_2comp_embeddings()

    @reactive.Calc
    def embeddings_5comp():
        return load_5comp_embeddings()

    @reactive.Calc
    def data():
        return load_topic_data()

    @reactive.Calc
    def filtered_data():
        # For range slider
        # topic_range = input.topic_range()
        # df = data()
        # return df[(df["topic"] >= topic_range[0]) & (df["topic"] <= topic_range[1])]
        
        # OR for multi-select
        selected = input.selected_topics()
        df = data()
        return df[df["topic"].isin(selected)]

    @reactive.Calc
    def titles():
        return load_titles()

    @reactive.Calc
    def topic_model():
        return load_topic_model()

    
    @reactive.Calc
    def fig_static_topic_map():
        # Get absolute path to the image file
        app_dir = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(app_dir, "www", "static", "img", "doc_map.png")
        
        # Use the refactored function from topic_utils.py
        return create_static_topic_map(image_path)
    

    @reactive.Calc
    def fig_topic_kwords():
        # title_data = titles()
        model_data = topic_model()
        # reduced_embeddings_data = embeddings_2comp()
        return create_topic_kwords(
            model=model_data,
            # text=title_data,
            # reduced_embeddings=reduced_embeddings_data
        )
        
    @reactive.Calc
    def fig_one():
        topic_trend_data = filtered_data()

        return create_topic_trend(
            data=topic_trend_data,
            title="",
            labels={"time_period": "Year", "count": "Project Count"},
        )
    
    @reactive.Calc
    def fig_two():
        topic_funding_data = data()

        return create_topic_total_funding(
            data=topic_funding_data,
            title="",
            labels={"ecMaxContribution": "Total EC Contribution", "topic": "Topic"}
        )

    @reactive.Calc
    def fig_three():
        topic_funding_data = data()

        return create_topic_avg_funding(
            data=topic_funding_data,
            title="",
            labels={"ecMaxContribution": "Total EC Contribution", "topic": "Topic"}
        )

    @reactive.Calc
    def fig_four():
        topic_funding_data = data()

        return create_topic_total_publication(
            data=topic_funding_data,
            title="",
            labels={"publication_count": "Total Publications", "topic": "Topic",}
        )
    
    @reactive.Calc
    def fig_five():
        topic_funding_data = data()

        return create_topic_avg_publication(
            data=topic_funding_data,
            title="",
            labels={"publication_count": "Total Publications", "topic": "Topic",}
        )

    @render_widget
    def topic_static_map():
        return fig_static_topic_map()

    @render_widget
    def topic_kwords_plot():
        return fig_topic_kwords()

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
    
    