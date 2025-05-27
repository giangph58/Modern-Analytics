import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame


def create_topic_trend(
    data: DataFrame,
    year_range: list[int],
    y_from: str,
    title: str,
    labels: dict,
) -> go.FigureWidget:
    data["ecSignatureDate"] = pd.to_datetime(data["ecSignatureDate"])
    data["time_period"] = data["ecSignatureDate"].dt.to_period("Y").dt.to_timestamp()

    # Count number of documents per topic per time period
    plot_data = data.groupby(["time_period", "topic"]).size().reset_index(name="count")

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
