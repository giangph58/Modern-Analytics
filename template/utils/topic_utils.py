import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
from bertopic import BERTopic
from umap import UMAP
import os
import base64
    

def create_static_topic_map(image_path: str, width: int = 1000, height: int = 800) -> go.Figure:
   # Create a basic figure
    fig = go.Figure()
    
    if os.path.exists(image_path):
        # Create a data URL for the image
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
            encoded = base64.b64encode(img_bytes).decode("utf-8")
            img_src = f"data:image/png;base64,{encoded}"
        
        # Add trace instead of layout_image (more reliable)
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode="markers",
                marker=dict(opacity=0),  # Invisible markers
                showlegend=False,
            )
        )
        
        # Use layout image with different parameters
        fig.update_layout(
            images=[
                dict(
                    source=img_src,
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=1, sizey=1,
                    sizing="stretch",  # "stretch" works better than "contain"
                    layer="below"
                )
            ],
            width=width, 
            height=height,
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0, 1]),
            plot_bgcolor="rgba(0,0,0,0)"
        )
    else:
        fig.add_annotation(
            text="Image not found",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=20)
        )
    
    return fig


def create_topic_kwords(
    model: BERTopic,
    topics: list = None,
    title: str = "",
    n_words: int = 6
) -> go.FigureWidget:
    """Create topic barchart visualization from BERTopic model"""
    # If no topics specified, use first 10 topics
    if topics is None:
        topics = list(range(23))
        
    fig = model.visualize_barchart(topics=topics, n_words=n_words)
    
    fig.update_layout(
        plot_bgcolor="white",
        title=title
    )
    
    return go.FigureWidget(fig)


def create_topic_trend(
    data: DataFrame,
    title: str,
    labels: dict,
) -> go.FigureWidget:
    
    data_copy = data.copy()
    data_copy["ecSignatureDate_dt"] = pd.to_datetime(data_copy["ecSignatureDate"])
    # data_copy["time_period"] = (
        # data_copy["ecSignatureDate_dt"].dt.to_period("Y").dt.to_timestamp()
    # )
    data_copy["time_period"] = data_copy["ecSignatureDate_dt"].dt.year

    # Count number of documents per topic per time period
    plot_data = data_copy.groupby(["time_period", "topic", "topic_label"]).size().reset_index(name="count")

    fig = px.line(
        data_frame=plot_data,
        x="time_period",
        y="count",
        color="topic",
        hover_name="topic_label",
        markers=True,
        title=title,
        labels=labels,
        # color_discrete_sequence=px.colors.colorbrewer.Blues[1:],
    )

    fig.update_traces(
        mode="markers+lines",
        hovertemplate=None,
        line=dict(width=2.5),
        marker=dict(size=10),
    )

    fig.update_layout(
        plot_bgcolor="white",
        hovermode="x unified",
        xaxis=dict(type='category')
    )

    fig.update_xaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)
    fig.update_yaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)

    return go.FigureWidget(fig)


def create_topic_total_funding(
    data: DataFrame,
    title: str,
    labels: dict,
) -> go.FigureWidget:
    
    data_copy = data.copy()
    data_copy["ecMaxContribution"] = (
        data_copy["ecMaxContribution"].str.replace(",", ".", regex=False).astype(float)
    )

    total_funding_by_topic = data_copy.groupby(["topic", "topic_label"])["ecMaxContribution"].sum().reset_index()

    fig = px.bar(
        total_funding_by_topic,
        x="topic",
        y="ecMaxContribution",
        title=title,
        labels=labels,
        hover_name="topic_label",
    )

    fig.update_layout(
        xaxis_title="Topic",
        yaxis_title="Total EC Contribution (€)",
        xaxis=dict(type="category"),
        hovermode="x unified",
    )


    fig.update_layout(
        plot_bgcolor="white",
        hovermode="x unified",
    )

    fig.update_xaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)
    fig.update_yaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)

    return go.FigureWidget(fig)


def create_topic_avg_funding(
    data: DataFrame,
    title: str,
    labels: dict,
) -> go.FigureWidget:

    data_copy = data.copy()
    data_copy["ecMaxContribution"] = (
        data_copy["ecMaxContribution"].str.replace(",", ".", regex=False).astype(float)
    )

    avg_funding_by_topic = data_copy.groupby(["topic", "topic_label"])["ecMaxContribution"].mean().reset_index()

    fig = px.bar(
        avg_funding_by_topic,
        x="topic",
        y="ecMaxContribution",
        title=title,
        labels=labels,
        hover_name="topic_label",
    )

    fig.update_layout(
        xaxis_title="Topic",
        yaxis_title="Average EC Contribution (€)",
        xaxis=dict(type="category"),
        hovermode="x unified",
    )


    fig.update_layout(
        plot_bgcolor="white",
        hovermode="x unified",
    )

    fig.update_xaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)
    fig.update_yaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)

    return go.FigureWidget(fig)

def create_topic_total_publication(
    data: DataFrame,
    title: str,
    labels: dict,
) -> go.FigureWidget:

    data_copy = data.copy()
    total_publication_by_topic = data_copy.groupby(["topic", "topic_label"])["publication_count"].sum().reset_index()

    fig = px.bar(
        total_publication_by_topic,
        x="topic",
        y="publication_count",
        title=title,
        labels=labels,
        hover_name="topic_label",
    )

    fig.update_layout(
        xaxis_title="Topic",
        yaxis_title="Number of Publications",
        xaxis=dict(type="category"),
        hovermode="x unified",
    )


    fig.update_layout(
        plot_bgcolor="white",
        hovermode="x unified",
    )

    fig.update_xaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)
    fig.update_yaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)

    return go.FigureWidget(fig)


def create_topic_avg_publication(
    data: DataFrame,
    title: str,
    labels: dict,
) -> go.FigureWidget:

    data_copy = data.copy()
    avg_publication_by_topic = data_copy.groupby(["topic", "topic_label"])["publication_count"].mean().reset_index()

    fig = px.bar(
        avg_publication_by_topic,
        x="topic",
        y="publication_count",
        title=title,
        labels=labels,
        hover_name="topic_label",
    )

    fig.update_layout(
        xaxis_title="Topic",
        yaxis_title="Number of Publications",
        xaxis=dict(type="category"),
        hovermode="x unified",
    )


    fig.update_layout(
        plot_bgcolor="white",
        hovermode="x unified",
    )

    fig.update_xaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)
    fig.update_yaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)

    return go.FigureWidget(fig)