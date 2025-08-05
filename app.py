import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

# Файл для хранения данных
DATA_FILE = "metrics_data.csv"

# Направления
DIRECTIONS = [
    "Оборудование для производства полупроводников", "Поверхностный монтаж", "Метрологическое оборудование",
    "Фотоника", "Испытательное оборудование", "Решения для электротранспорта", "Ainuo", "Зондовые станции",
    "LoadPull", "Кванты", "Радиоизмерительные приборы", "Телеком", "Усилители", "Промышленная мебель",
    "Акметех", "ПО", "Сервис"
]

# Метрики
METRICS = ["Средства производства", "Маркетинг", "Продажи", "Команда"]

# Загрузка или инициализация данных
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Направление", "Месяц"] + METRICS + ["Общая цифра"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Радар-диаграмма (Plotly)
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
        width=360,
        height=360,
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font_color='white',
        margin=dict(t=30, b=20, l=30, r=30),
        polar=dict(
            bgcolor='#1c1f26',
            radialaxis=dict(visible=True, range=[0, 10], showline=False, gridcolor="gray"),
            angularaxis=dict(gridcolor="gray")
        ),
        showlegend=False
    )

    return fig

# --- Интерфейс ---
st.set_page_config(page_title="Метрики развития", layout="wide")
st.markdown("""
    <style>
        h1, h2, h3, .stMetricLabel { font-size: 1.2em !important; }
        .block-container { padding-top: 2rem !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='margin-bottom: 0.5rem;'>Мониторинг метрик по направлениям</h1>", unsafe_allow_html=True)

menu = st.sidebar.radio("Выберите раздел:", ["Ввод данных", "Отчеты"])

# --- Ввод данных ---
if menu == "Ввод данных":
    st.header("Ввод метрик по направлению")

    direction = st.selectbox("Направление:", DIRECTIONS)
    month = st.text_input("Месяц (например, 2025-08):", value=datetime.now().strftime("%Y-%m"))

    col1, col2 = st.columns(2)
    with col1:
        m1 = st.slider(METRICS[0], 0.0, 10.0, 5.0, 0.1)
        m2 = st.slider(METRICS[1], 0.0, 10.0, 5.0, 0.1)
    with col2:
        m3 = st.slider(METRICS[2], 0.0, 10.0, 5.0, 0.1)
        m4 = st.slider(METRICS[3], 0.0, 10.0, 5.0, 0.1)

    overall = round((m1 + m2 + m3 + m4) / 4, 2)
    st.metric("Общая цифра", overall)

    if st.button("Сохранить отчет"):
        df = load_data()
        new_row = pd.DataFrame.from_dict({
            "Направление": [direction],
            "Месяц": [month],
            METRICS[0]: [m1], METRICS[1]: [m2], METRICS[2]: [m3], METRICS[3]: [m4],
            "Общая цифра": [overall]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success("Отчет сохранен!")

# --- Отчеты ---
elif menu == "Отчеты":
    st.header("📈 Отчеты и диаграммы")
    df = load_data()

    if df.empty:
        st.info("Данных пока нет. Введите хотя бы один отчет.")
    else:
        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            selected_direction = st.selectbox("Выберите направление:", df["Направление"].unique())
            months = df[df["Направление"] == selected_direction]["Месяц"].unique()
            selected_month = st.selectbox("Выберите месяц:", months)
            row = df[(df["Направление"] == selected_direction) & (df["Месяц"] == selected_month)].iloc[-1]

            st.markdown(f"<h3 style='margin-top: 0.5rem;'>Данные по метрикам ({selected_month})</h3>", unsafe_allow_html=True)
            st.dataframe(
                row[METRICS + ["Общая цифра"]].to_frame(name="Значение"),
                use_container_width=True,
                hide_index=False
            )

        with col_right:
            # Центрированный заголовок и диаграмма
            st.markdown(
                f"""
                <div style='text-align:center; margin-top: -0.5rem; margin-bottom: 0.8rem'>
                    <h3>{selected_direction} — {selected_month}</h3>
                </div>
                """, unsafe_allow_html=True
            )
            fig = plot_radar([row[m] for m in METRICS])
            st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})
