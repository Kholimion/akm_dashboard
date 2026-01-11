"""
Главный файл приложения для мониторинга метрик по направлениям
"""

import streamlit as st

from config import PAGE_CONFIG
from ui_components import (
    setup_page_style,
    render_header,
    render_data_input_page,
    render_reports_page
)


def main():
    """Главная функция приложения"""
    # Настройка страницы
    st.set_page_config(**PAGE_CONFIG)
    setup_page_style()
    
    # Заголовок
    render_header()
    
    # Боковое меню
    menu = st.sidebar.radio(
        "Выберите раздел:",
        ["Ввод данных", "Отчеты"]
    )
    
    # Маршрутизация по разделам
    if menu == "Ввод данных":
        render_data_input_page()
    elif menu == "Отчеты":
        render_reports_page()


if __name__ == "__main__":
    main()
