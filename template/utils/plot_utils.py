import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame


def create_figure(
    data: DataFrame,
    year_range: list[int],
    country: str,
    y_from: str,
    title: str,
    labels: dict,
) -> go.FigureWidget:
    plot_data = data[data["Year"].between(year_range[0], year_range[1])]
    plot_data = plot_data[plot_data["Entity"].isin(country)]

    fig = px.line(
        data_frame=plot_data,
        x="Year",
        y=y_from,
        color="Entity",
        title=title,
        labels=labels,
        color_discrete_sequence=px.colors.colorbrewer.Blues[1:],
    )

    fig.update_traces(
        mode="markers+lines",
        hovertemplate=None,
        line=dict(width=5),
        marker=dict(size=15),
    )
    fig.update_layout(
        plot_bgcolor="white",
        hovermode="x unified",
        xaxis=dict(tickformat="%Y", ticklabelmode="period"),
    )

    fig.update_xaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)
    fig.update_yaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)

    return go.FigureWidget(fig)


def create_topic_trend(
    data: DataFrame,
    y_from: str,
    title: str,
    labels: dict,
) -> go.FigureWidget:
    data["ecSignatureDate"] = pd.to_datetime(data["ecSignatureDate"])
    data["time_period"] = data["ecSignatureDate"].dt.to_period("Y").dt.to_timestamp()
    plot_data = data.groupby(["time_period", "topic"]).size().reset_index(name="count")
    # plot_data["topic_label"] = plot_data["topic"].map(topic_labels)

    fig = px.line(
        plot_data,
        x="time_period",
        y="count",
        color="topic",
        markers=True,
        title="Topic Trends Over Time",
        hover_name="topic_label",
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Project Count",
        legend_title="Topic",
        xaxis=dict(tickformat="%Y", ticklabelmode="period"),
        hovermode="x unified",
    )
    return go.FigureWidget(fig)
