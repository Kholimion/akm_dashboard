"""
Модуль UI компонентов
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from config import (
    CATEGORIES,
    METRICS,
    NUMERIC_METRICS,
    TEXT_METRIC,
    STAGE_OPTIONS,
    NEW_TEXT_FIELDS
)
from data_manager import (
    load_data,
    save_data,
    create_data_row,
    calculate_overall_score,
    update_default_value,
    get_default_value
)
from visualization import (
    create_radar_chart,
    create_bar_chart,
    get_chart_config
)


def setup_page_style() -> None:
    """Настраивает стили страницы"""
    st.markdown("""
        <style>
            h1, h2, h3, .stMetricLabel { 
                font-size: 1.2em !important; 
            }
            .block-container { 
                padding-top: 2rem !important; 
                padding-bottom: 2rem !important;
            }
            .stTextInput > div > div > input {
                margin-bottom: 0.5rem;
            }
            .stSelectbox > div > div {
                margin-bottom: 0.5rem;
            }
            .element-container {
                margin-bottom: 1rem;
            }
            @media (max-width: 768px) {
                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
            }
        </style>
    """, unsafe_allow_html=True)


def render_header() -> None:
    """Отображает заголовок приложения"""
    st.markdown(
        "<h1 style='margin-bottom: 0.5rem;'>📊 Мониторинг метрик по направлениям</h1>",
        unsafe_allow_html=True
    )


def render_data_input_tab(tab, category_label: str) -> None:
    """
    Отображает форму ввода данных для категории
    
    Args:
        tab: Streamlit tab объект
        category_label: Название категории
    """
    with tab:
        # Контейнер для формы с отступами
        st.markdown("<div style='margin-bottom: 2rem;'>", unsafe_allow_html=True)
        
        # Выбор направления
        direction = st.selectbox(
            f"Направление ({category_label}):",
            CATEGORIES[category_label],
            key=f"input_{category_label}"
        )
        
        # Стадия
        stage = st.selectbox(
            "Стадия:",
            STAGE_OPTIONS,
            key=f"stage_{category_label}"
        )
        
        # Лидер (с запоминанием последнего значения для направления)
        leader_default = get_default_value(direction, NEW_TEXT_FIELDS[0])
        leader = st.text_input(
            NEW_TEXT_FIELDS[0] + ":",
            value=leader_default,
            key=f"leader_{category_label}",
            placeholder="Введите значение..."
        )
        
        st.markdown("---")
        
        # Ввод месяца
        month = st.text_input(
            "Месяц (например, 2025-08):",
            value=datetime.now().strftime("%Y-%m"),
            key=f"month_{category_label}"
        )
        
        # Слайдеры для метрик
        st.markdown("### Метрики")
        col1, col2 = st.columns(2)
        with col1:
            m1 = st.slider(
                METRICS[0],
                0.0, 10.0, 5.0, 0.1,
                key=f"m1_{category_label}"
            )
            m2 = st.slider(
                METRICS[1],
                0.0, 10.0, 5.0, 0.1,
                key=f"m2_{category_label}"
            )
        with col2:
            m3 = st.slider(
                METRICS[2],
                0.0, 10.0, 5.0, 0.1,
                key=f"m3_{category_label}"
            )
            m4 = st.slider(
                METRICS[3],
                0.0, 10.0, 5.0, 0.1,
                key=f"m4_{category_label}"
            )
        
        # Расчет и отображение общей цифры
        overall = calculate_overall_score([m1, m2, m3, m4])
        st.metric("Общая цифра", overall)
        
        st.markdown("---")
        
        # Числовые метрики
        st.markdown("### Финансовые показатели")
        col3, col4 = st.columns(2)
        with col3:
            portfolio = st.number_input(
                NUMERIC_METRICS[0],
                min_value=0.0,
                step=0.1,
                key=f"portf_{category_label}"
            )
        with col4:
            ambition = st.number_input(
                NUMERIC_METRICS[1],
                min_value=0.0,
                step=0.1,
                key=f"amb_{category_label}"
            )
        
        # Текстовая метрика
        value_text = st.text_input(
            TEXT_METRIC,
            key=f"text_{category_label}"
        )
        
        st.markdown("---")
        
        # Новые текстовые поля с автозаполнением
        st.markdown("### Дополнительная информация")
        
        # Магниты (с запоминанием последнего значения для направления)
        magnets_default = get_default_value(direction, NEW_TEXT_FIELDS[1])
        magnets = st.text_area(
            NEW_TEXT_FIELDS[1] + ":",
            value=magnets_default,
            key=f"magnets_{category_label}",
            placeholder="Введите значение...",
            height=100
        )
        
        # Источник финансирования (с запоминанием последнего значения для направления)
        funding_default = get_default_value(direction, NEW_TEXT_FIELDS[2])
        funding_source = st.text_input(
            NEW_TEXT_FIELDS[2] + ":",
            value=funding_default,
            key=f"funding_{category_label}",
            placeholder="Введите значение..."
        )
        
        # Стратегия (с запоминанием последнего значения для направления)
        strategy_default = get_default_value(direction, NEW_TEXT_FIELDS[3])
        strategy = st.text_area(
            NEW_TEXT_FIELDS[3] + ":",
            value=strategy_default,
            key=f"strategy_{category_label}",
            placeholder="Введите значение...",
            height=100
        )
        
        # Управленческие решения (с запоминанием последнего значения для направления)
        decisions_default = get_default_value(direction, NEW_TEXT_FIELDS[4])
        management_decisions = st.text_input(
            NEW_TEXT_FIELDS[4] + ":",
            value=decisions_default,
            key=f"decisions_{category_label}",
            placeholder="Введите значение..."
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Кнопка сохранения
        if st.button("📂 Сохранить отчет", key=f"save_{category_label}", use_container_width=True):
            # Обновляем последние значения для направления
            if leader and leader.strip():
                update_default_value(direction, NEW_TEXT_FIELDS[0], leader)
            if magnets and magnets.strip():
                update_default_value(direction, NEW_TEXT_FIELDS[1], magnets)
            if funding_source and funding_source.strip():
                update_default_value(direction, NEW_TEXT_FIELDS[2], funding_source)
            if strategy and strategy.strip():
                update_default_value(direction, NEW_TEXT_FIELDS[3], strategy)
            if management_decisions and management_decisions.strip():
                update_default_value(direction, NEW_TEXT_FIELDS[4], management_decisions)
            
            df = load_data()
            new_row = create_data_row(
                direction=direction,
                month=month,
                stage=stage,
                metrics=[m1, m2, m3, m4],
                portfolio=portfolio,
                ambition=ambition,
                value_text=value_text,
                leader=leader or "",
                magnets=magnets or "",
                funding_source=funding_source or "",
                strategy=strategy or "",
                management_decisions=management_decisions or ""
            )
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("✅ Отчет сохранен!")


def render_data_input_page() -> None:
    """Отображает страницу ввода данных"""
    st.header("📝 Ввод метрик по направлению")
    
    tab1, tab2, tab3 = st.tabs(list(CATEGORIES.keys()))
    
    for category_label, tab in zip(CATEGORIES.keys(), [tab1, tab2, tab3]):
        render_data_input_tab(tab, category_label)


def render_reports_tab(tab, category_label: str, df: pd.DataFrame) -> None:
    """
    Отображает отчеты для конкретной категории
    
    Args:
        tab: Streamlit tab объект
        category_label: Название категории
        df: DataFrame с данными
    """
    with tab:
        # Фильтруем данные по категории
        category_directions = CATEGORIES[category_label]
        category_df = df[df["Направление"].isin(category_directions)]
        
        if category_df.empty:
            st.info(f"Данных по категории '{category_label}' пока нет.")
            return
        
        # Выбор направления и месяца
        col_select1, col_select2 = st.columns(2)
        with col_select1:
            selected_direction = st.selectbox(
                "Выберите направление:",
                category_df["Направление"].unique(),
                key=f"report_dir_{category_label}"
            )
        
        with col_select2:
            months = category_df[category_df["Направление"] == selected_direction]["Месяц"].unique()
            if len(months) > 0:
                selected_month = st.selectbox(
                    "Выберите месяц:",
                    months,
                    key=f"report_month_{category_label}"
                )
            else:
                st.info("Нет данных для выбранного направления")
                return
        
        # Получение данных для выбранного направления и месяца
        row = category_df[
            (category_df["Направление"] == selected_direction) &
            (category_df["Месяц"] == selected_month)
        ].iloc[-1]
        
        # Заголовок с информацией о направлении
        st.markdown(
            f"<h2 style='margin-bottom: 1rem;'>{selected_direction} — {selected_month}</h2>",
            unsafe_allow_html=True
        )
        
        # Основная информация в карточках
        info_cols = st.columns(3)
        with info_cols[0]:
            if "Стадия" in row and pd.notna(row["Стадия"]):
                st.metric("Стадия", row["Стадия"])
        with info_cols[1]:
            if "Общая цифра" in row and pd.notna(row["Общая цифра"]):
                st.metric("Общая цифра", f"{row['Общая цифра']:.2f}")
        with info_cols[2]:
            if NEW_TEXT_FIELDS[0] in row and pd.notna(row[NEW_TEXT_FIELDS[0]]) and row[NEW_TEXT_FIELDS[0]]:
                st.metric("Лидер", row[NEW_TEXT_FIELDS[0]])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Метрики и радиальная диаграмма
        col_left, col_right = st.columns([1, 1.5], gap="large")
        
        with col_left:
            st.markdown("### 📊 Метрики")
            metrics_data = {}
            for metric in METRICS:
                if metric in row and pd.notna(row[metric]):
                    metrics_data[metric] = row[metric]
            
            if metrics_data:
                metrics_df = pd.DataFrame(list(metrics_data.items()), columns=["Метрика", "Значение"])
                st.dataframe(metrics_df, use_container_width=True, hide_index=True)
            
            st.markdown("### 💰 Финансовые показатели")
            financial_data = {}
            for metric in NUMERIC_METRICS:
                if metric in row and pd.notna(row[metric]):
                    financial_data[metric] = row[metric]
            
            if financial_data:
                financial_df = pd.DataFrame(list(financial_data.items()), columns=["Показатель", "Значение"])
                st.dataframe(financial_df, use_container_width=True, hide_index=True)
        
        with col_right:
            st.markdown("### 📈 Радиальная диаграмма")
            if all(m in row and pd.notna(row[m]) for m in METRICS):
                fig = create_radar_chart([row[m] for m in METRICS])
                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config=get_chart_config()
                )
            else:
                st.info("Недостаточно данных для построения диаграммы")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Дополнительная информация
        st.markdown("### 📝 Дополнительная информация")
        
        additional_info = {}
        if TEXT_METRIC in row and pd.notna(row[TEXT_METRIC]) and row[TEXT_METRIC]:
            additional_info[TEXT_METRIC] = row[TEXT_METRIC]
        
        for field in NEW_TEXT_FIELDS:
            if field in row and pd.notna(row[field]) and row[field]:
                additional_info[field] = row[field]
        
        if additional_info:
            for key, value in additional_info.items():
                with st.expander(key, expanded=False):
                    st.write(value)
        else:
            st.info("Дополнительная информация не заполнена")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Столбчатые диаграммы
        st.markdown("### 📊 Динамика финансовых показателей")
        chart_cols = st.columns(2)
        
        with chart_cols[0]:
            if NUMERIC_METRICS[0] in category_df.columns:
                bar1 = create_bar_chart(
                    category_df[category_df["Направление"] == selected_direction],
                    NUMERIC_METRICS[0],
                    NUMERIC_METRICS[0]
                )
                st.plotly_chart(bar1, use_container_width=True, config=get_chart_config())
        
        with chart_cols[1]:
            if NUMERIC_METRICS[1] in category_df.columns:
                bar2 = create_bar_chart(
                    category_df[category_df["Направление"] == selected_direction],
                    NUMERIC_METRICS[1],
                    NUMERIC_METRICS[1]
                )
                st.plotly_chart(bar2, use_container_width=True, config=get_chart_config())


def render_reports_page() -> None:
    """Отображает страницу отчетов"""
    st.header("📈 Отчеты и диаграммы")
    
    df = load_data()
    
    if df.empty:
        st.info("Данных пока нет. Введите хотя бы один отчет.")
        return
    
    # Подвкладки для категорий
    report_tabs = st.tabs(list(CATEGORIES.keys()))
    
    for category_label, tab in zip(CATEGORIES.keys(), report_tabs):
        render_reports_tab(tab, category_label, df)
