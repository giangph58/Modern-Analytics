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
    plot_data = plot_data[plot_data["Entity"].isin(country)].copy()

    fig = px.line(
        data_frame=plot_data,
        x="Year",
        y=y_from,
        color="Entity",
        title=title,
        labels=labels,
        # color_discrete_sequence=px.colors.colorbrewer.Blues[1:],
        color_discrete_sequence=px.colors.colorbrewer.Pastel1,
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


def create_funds_bar_chart(
    data: DataFrame,
    country: str,
    y_from: str,
    title: str,
    labels: dict,
) -> go.FigureWidget:
    plot_data = data[data["Entity"].isin(country)]
    plot_data["TotalFunds"] = plot_data["TotalFunds"].multiply(0.1)

    fig = px.bar(
        data_frame=plot_data,
        x="Entity",
        y=y_from,
        color="Entity",
        title=title,
        labels=labels,
        color_discrete_sequence=px.colors.colorbrewer.Pastel1,
    )
    fig.update_traces(
        hovertemplate=f"<b>%{{x}}</b><br>{labels.get(y_from, y_from)}: %{{y:,.0f}}<extra></extra>"
    )
    fig.update_layout(
        plot_bgcolor="white",
        hovermode="x",
        xaxis={
            "categoryorder": "total descending",
            # "title_text": labels.get(x_col, x_col),
        },
        yaxis={"title_text": labels.get(y_from, y_from)},
    )
    fig.update_xaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)
    fig.update_yaxes(showline=False, gridcolor="#d2d2d2", gridwidth=0.5)

    return go.FigureWidget(fig)
