import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

# === Конфигурация ===
DATA_FILE = "metrics_data.csv"

CATEGORIES = {
    "Дистрибуция": [
        "Оборудование для производства полупроводников", "Поверхностный монтаж", "Метрологическое оборудование",
        "Фотоника", "Испытательное оборудование", "Решения для электротранспорта", "Ainuo", "Зондовые станции",
        "LoadPull", "Кванты", "Радиоизмерительные приборы", "Телеком", "Усилители"
    ],
    "Производство": ["Промышленная мебель", "Акметех"],
    "Услуги": ["ПО", "Сервис"]
}

METRICS = ["Средства производства", "Маркетинг", "Продажи", "Команда"]
TEXT_METRIC = "Ценность БМ для клиента"
NUMERIC_METRICS = ["Суммарный портфель _ год (млрд)", "Суммарная амбиция _ год (млрд)"]

# === Загрузка / Сохранение данных ===
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=["Направление", "Месяц"] + METRICS + ["Общая цифра"] + NUMERIC_METRICS + [TEXT_METRIC])
    else:
        return pd.DataFrame(columns=["Направление", "Месяц"] + METRICS + ["Общая цифра"] + NUMERIC_METRICS + [TEXT_METRIC])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# === Диаграммы ===
def plot_radar(metrics_values):
    labels = METRICS + [METRICS[0]]
    values = metrics_values + [metrics_values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name="",
        line_color='lightblue',
        fillcolor='rgba(173, 216, 230, 0.4)'
    ))

    fig.update_layout(
        autosize=False,
        width=350,
        height=350,
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font_color='white',
        margin=dict(t=20, b=20),
        polar=dict(
            bgcolor='#1c1f26',
            radialaxis=dict(visible=True, range=[0, 10], showline=False, gridcolor="gray"),
            angularaxis=dict(gridcolor="gray")
        ),
        showlegend=False
    )
    return fig

def plot_bar(df, column, title):
    filtered = df.dropna(subset=[column])
    grouped = filtered.groupby("Месяц")[column].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped["Месяц"],
        y=grouped[column],
        text=grouped[column].round(2),
        textposition='outside',
        textfont=dict(size=16),
        marker=dict(color='rgba(173, 216, 230, 0.6)')
    ))

    fig.update_layout(
        title=f"\U0001F4C8 {title}",
        xaxis_title="Месяц",
        yaxis_title="Значение",
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white', size=14),
        margin=dict(t=50, b=50)
    )
    return fig

# === Интерфейс ===
st.set_page_config(page_title="Метрики развития", layout="wide")
st.markdown("""
    <style>
        h1, h2, h3, .stMetricLabel { font-size: 1.2em !important; }
        .block-container { padding-top: 2rem !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='margin-bottom: 0.5rem;'>📊 Мониторинг метрик по направлениям</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("Выберите раздел:", ["Ввод данных", "Отчеты"])

# === Ввод данных ===
if menu == "Ввод данных":
    st.header("📝 Ввод метрик по направлению")
    tab1, tab2, tab3 = st.tabs(["Дистрибуция", "Производство", "Услуги"])

    for label, tab in zip(CATEGORIES.keys(), [tab1, tab2, tab3]):
        with tab:
            direction = st.selectbox(f"Направление ({label}):", CATEGORIES[label], key=f"input_{label}")
            month = st.text_input("Месяц (например, 2025-08):", value=datetime.now().strftime("%Y-%m"), key=f"month_{label}")

            col1, col2 = st.columns(2)
            with col1:
                m1 = st.slider(METRICS[0], 0.0, 10.0, 5.0, 0.1, key=f"m1_{label}")
                m2 = st.slider(METRICS[1], 0.0, 10.0, 5.0, 0.1, key=f"m2_{label}")
            with col2:
                m3 = st.slider(METRICS[2], 0.0, 10.0, 5.0, 0.1, key=f"m3_{label}")
                m4 = st.slider(METRICS[3], 0.0, 10.0, 5.0, 0.1, key=f"m4_{label}")

            col3, col4 = st.columns(2)
            with col3:
                portf = st.number_input(NUMERIC_METRICS[0], min_value=0.0, step=0.1, key=f"portf_{label}")
            with col4:
                ambition = st.number_input(NUMERIC_METRICS[1], min_value=0.0, step=0.1, key=f"amb_{label}")

            value_text = st.text_input(TEXT_METRIC, key=f"text_{label}")

            overall = round((m1 + m2 + m3 + m4) / 4, 2)
            st.metric("Общая цифра", overall)

            if st.button("📂 Сохранить отчет", key=f"save_{label}"):
                df = load_data()
                new_row = pd.DataFrame.from_dict({
                    "Направление": [direction],
                    "Месяц": [month],
                    METRICS[0]: [m1], METRICS[1]: [m2], METRICS[2]: [m3], METRICS[3]: [m4],
                    "Общая цифра": [overall],
                    NUMERIC_METRICS[0]: [portf],
                    NUMERIC_METRICS[1]: [ambition],
                    TEXT_METRIC: [value_text]
                })
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("Отчет сохранен!")

# === Отчеты ===
elif menu == "Отчеты":
    st.header("📈 Отчеты и диаграммы")
    df = load_data()

    if df.empty:
        st.info("Данных пока нет. Введите хотя бы один отчет.")
    else:
        selected_direction = st.selectbox("Выберите направление:", df["Направление"].unique())
        months = df[df["Направление"] == selected_direction]["Месяц"].unique()
        selected_month = st.selectbox("Выберите месяц:", months)

        row = df[(df["Направление"] == selected_direction) & (df["Месяц"] == selected_month)].iloc[-1]

        col_left, col_right = st.columns([1, 2], gap="large")
        with col_left:
            st.markdown(f"<h3 style='margin-top: 0.5rem;'>Данные по метрикам ({selected_month})</h3>", unsafe_allow_html=True)
            display_df = row[METRICS + ["Общая цифра"] + NUMERIC_METRICS + [TEXT_METRIC]].to_frame(name="Значение")
            st.dataframe(display_df, use_container_width=True)

        with col_right:
            st.markdown(f"<div style='text-align:center;'><h3>{selected_direction} — {selected_month}</h3></div>", unsafe_allow_html=True)
            st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
            fig = plot_radar([row[m] for m in METRICS])
            st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            bar1 = plot_bar(df[df["Направление"] == selected_direction], NUMERIC_METRICS[0], NUMERIC_METRICS[0])
            st.plotly_chart(bar1, use_container_width=True, config={"displayModeBar": False})

        with col2:
            bar2 = plot_bar(df[df["Направление"] == selected_direction], NUMERIC_METRICS[1], NUMERIC_METRICS[1])
            st.plotly_chart(bar2, use_container_width=True, config={"displayModeBar": False})
