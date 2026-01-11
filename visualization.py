"""
Модуль для создания визуализаций
"""

import plotly.graph_objects as go
import pandas as pd
from config import (
    METRICS,
    NUMERIC_METRICS,
    COLORS,
    CHART_CONFIG
)


def create_radar_chart(metrics_values: list[float]) -> go.Figure:
    """
    Создает радиальную диаграмму (spider chart) для метрик
    
    Args:
        metrics_values: Список значений метрик
        
    Returns:
        go.Figure: Объект фигуры Plotly
    """
    # Замыкаем круг для визуализации
    labels = METRICS + [METRICS[0]]
    values = metrics_values + [metrics_values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name="",
        line_color=COLORS["line"],
        fillcolor=COLORS["primary_fill"]
    ))
    
    fig.update_layout(
        autosize=False,
        width=350,
        height=350,
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["background"],
        font_color=COLORS["text"],
        margin=dict(t=20, b=20),
        polar=dict(
            bgcolor=COLORS["plot_bg"],
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showline=False,
                gridcolor=COLORS["grid"]
            ),
            angularaxis=dict(gridcolor=COLORS["grid"])
        ),
        showlegend=False
    )
    
    return fig


def create_bar_chart(
    df: pd.DataFrame,
    column: str,
    title: str
) -> go.Figure:
    """
    Создает столбчатую диаграмму для числовых метрик
    
    Args:
        df: DataFrame с данными
        column: Название колонки для отображения
        title: Заголовок диаграммы
        
    Returns:
        go.Figure: Объект фигуры Plotly
    """
    # Фильтруем и группируем данные
    filtered = df.dropna(subset=[column])
    grouped = filtered.groupby("Месяц")[column].mean().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=grouped["Месяц"],
        y=grouped[column],
        text=grouped[column].round(2),
        textposition='outside',
        textfont=dict(size=16),
        marker=dict(color=COLORS["primary"])
    ))
    
    fig.update_layout(
        title=f"📈 {title}",
        xaxis_title="Месяц",
        yaxis_title="Значение",
        plot_bgcolor=COLORS["background"],
        paper_bgcolor=COLORS["background"],
        font=dict(color=COLORS["text"], size=14),
        margin=dict(t=50, b=50)
    )
    
    return fig


def get_chart_config() -> dict:
    """
    Возвращает конфигурацию для отображения графиков
    
    Returns:
        dict: Конфигурация для plotly charts
    """
    return CHART_CONFIG
