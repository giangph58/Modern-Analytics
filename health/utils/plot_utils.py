import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.nonparametric.smoothers_lowess import lowess
import statsmodels.api as sm


def create_funds_bar_chart(
    data: DataFrame,
    country: str,
    y_from: str,
    title: str,
    labels: dict,
) -> go.FigureWidget:
    plot_data = data[data["country_name"].isin(country)]
    # plot_data["TotalFunds"] = plot_data["TotalFundsPerCountry"]

    fig = px.bar(
        data_frame=plot_data,
        x=y_from,
        y="country_name",
        color="country_name",
        title=title,
        labels=labels,
        color_discrete_sequence=["#003366"],
        orientation='h'
    )
    fig.update_traces(
        hovertemplate=f"<b>%{{y}}</b><br>{labels.get(y_from, y_from)}: %{{x:,.0f}}<extra></extra>"
    )
    
    # Font configs
    xaxis_font_size = 16
    yaxis_font_size = 16
    axis_title_size = 18
    title_font_size = 24
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        height=800,
        width=1200,
        hovermode="y unified",
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=title_font_size)
        ),
        xaxis=dict(
            title_text=labels.get(y_from, y_from),
            title_font=dict(size=axis_title_size),
            tickfont=dict(size=xaxis_font_size),
            showgrid=True,
            gridcolor="#d2d2d2",
            gridwidth=0.5
        ),
        yaxis=dict(
            categoryorder="total ascending",
            title=None,
            tickfont=dict(size=yaxis_font_size),
            showgrid=False
        ),
    )
    fig.update_xaxes(showline=False)
    fig.update_yaxes(showline=False)

    return go.FigureWidget(fig)


def create_scatter_plot(
    data: DataFrame,
    country: str,
    x_col: str,
    y_col: str,
    text_col: str,
    title: str,
    labels: dict,
) -> go.FigureWidget:
    """
    Create a scatter plot with regression lines and confidence intervals
    """
    # Remove rows with missing data
    plot_data = data[data["country_name"].isin(country)]
    plot_data = plot_data.dropna(subset=[x_col, y_col])
  
    if plot_data.empty:
        fig = go.Figure()
        fig.update_layout(title="No data available")
        return go.FigureWidget(fig)
  
    # Create base scatter plot
    fig = px.scatter(
        plot_data,
        x=x_col,
        y=y_col,
        text=text_col,
        title=title,
        labels=labels,
        color_discrete_sequence=px.colors.colorbrewer.Pastel1,
    )
    
    # --- LINEAR REGRESSION with confidence interval ---
    if len(plot_data) > 1:
        X = sm.add_constant(plot_data[x_col])
        model = sm.OLS(plot_data[y_col], X).fit()
        
        # Sort data for proper line plotting
        x_sorted = np.sort(plot_data[x_col].values)
        X_sorted = sm.add_constant(x_sorted)
        
        preds = model.get_prediction(X_sorted)
        summary_frame = preds.summary_frame(alpha=0.05)  # 95% CI
        
        # Add linear regression line
        fig.add_trace(go.Scatter(
            x=x_sorted,
            y=summary_frame["mean"],
            mode="lines",
            name="Linear Fit",
            line=dict(color="red"),
            hovertemplate="Linear Fit<extra></extra>"
        ))
        
        # Add linear CI band
        fig.add_trace(go.Scatter(
            x=np.concatenate([x_sorted, x_sorted[::-1]]),
            y=np.concatenate([summary_frame["mean_ci_upper"], summary_frame["mean_ci_lower"][::-1]]),
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            name="Linear 95% CI",
            showlegend=True  # Changed to True to show in legend
        ))
    
    # --- LOESS smoothing ---
    if len(plot_data) > 3:
        try:
            loess_result = lowess(plot_data[y_col], plot_data[x_col], frac=0.8)
            x_loess = loess_result[:, 0]
            y_loess = loess_result[:, 1]
            
            # Add LOESS line
            fig.add_trace(go.Scatter(
                x=x_loess,
                y=y_loess,
                mode="lines",
                name="LOESS Fit",
                line=dict(color="blue"),
                hovertemplate="LOESS Fit<extra></extra>"
            ))
                
        except Exception:
            # If LOESS fails, skip it
            pass
    
    # Font configs
    xaxis_font_size = 16
    yaxis_font_size = 16
    axis_title_size = 18
    title_font_size = 24
    
    # Update layout
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=title_font_size)
        ),
        xaxis=dict(
            title=labels.get(x_col, x_col),
            title_font=dict(size=axis_title_size),
            tickfont=dict(size=xaxis_font_size),
            showgrid=True,
            gridcolor="lightgrey",
            linecolor="black",
            mirror=True
        ),
        yaxis=dict(
            title=labels.get(y_col, y_col),
            title_font=dict(size=axis_title_size),
            tickfont=dict(size=yaxis_font_size),
            showgrid=True,
            gridcolor="lightgrey",
            linecolor="black",
            mirror=True
        ),
        legend=dict(
            font=dict(size=16)
        ),
        hovermode="closest",
        height=700,
        width=1200,
        margin=dict(l=100, r=50, t=80, b=70)
    )
    
    # Update scatter trace styling
    fig.update_traces(
        textposition="middle right",
        textfont=dict(size=14),
        marker=dict(size=10),
        selector=dict(mode="markers+text")
    )
    
    return go.FigureWidget(fig)

