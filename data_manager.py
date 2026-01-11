"""
Модуль для работы с данными
"""

import os
import json
import pandas as pd
from config import (
    DATA_FILE,
    METRICS,
    NUMERIC_METRICS,
    TEXT_METRIC,
    STAGE_OPTIONS,
    NEW_TEXT_FIELDS,
    AUTOCOMPLETE_FILE
)


def load_data() -> pd.DataFrame:
    """
    Загружает данные из CSV файла
    
    Returns:
        pd.DataFrame: DataFrame с данными или пустой DataFrame с нужными колонками
    """
    columns = (
        ["Направление", "Месяц", "Стадия"] +
        METRICS +
        ["Общая цифра"] +
        NUMERIC_METRICS +
        [TEXT_METRIC] +
        NEW_TEXT_FIELDS
    )
    
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            # Убеждаемся, что все необходимые колонки присутствуют
            for col in columns:
                if col not in df.columns:
                    df[col] = None
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=columns)
    else:
        return pd.DataFrame(columns=columns)


def save_data(df: pd.DataFrame) -> None:
    """
    Сохраняет DataFrame в CSV файл
    
    Args:
        df: DataFrame для сохранения
    """
    df.to_csv(DATA_FILE, index=False)


def calculate_overall_score(metrics_values: list[float]) -> float:
    """
    Вычисляет общую оценку как среднее арифметическое метрик
    
    Args:
        metrics_values: Список значений метрик
        
    Returns:
        float: Среднее значение метрик, округленное до 2 знаков
    """
    if not metrics_values:
        return 0.0
    return round(sum(metrics_values) / len(metrics_values), 2)


def create_data_row(
    direction: str,
    month: str,
    stage: str,
    metrics: list[float],
    portfolio: float,
    ambition: float,
    value_text: str,
    leader: str,
    magnets: str,
    funding_source: str,
    strategy: str,
    management_decisions: str
) -> pd.DataFrame:
    """
    Создает новую строку данных для добавления в DataFrame
    
    Args:
        direction: Направление
        month: Месяц в формате YYYY-MM
        stage: Стадия развития
        metrics: Список значений метрик
        portfolio: Значение портфеля
        ambition: Значение амбиции
        value_text: Текстовая метрика
        leader: Лидер
        magnets: Магниты
        funding_source: Источник финансирования
        strategy: Стратегия
        management_decisions: Управленческие решения
        
    Returns:
        pd.DataFrame: DataFrame с одной строкой данных
    """
    overall = calculate_overall_score(metrics)
    
    data = {
        "Направление": [direction],
        "Месяц": [month],
        "Стадия": [stage],
        METRICS[0]: [metrics[0]],
        METRICS[1]: [metrics[1]],
        METRICS[2]: [metrics[2]],
        METRICS[3]: [metrics[3]],
        "Общая цифра": [overall],
        NUMERIC_METRICS[0]: [portfolio],
        NUMERIC_METRICS[1]: [ambition],
        TEXT_METRIC: [value_text],
        NEW_TEXT_FIELDS[0]: [leader],
        NEW_TEXT_FIELDS[1]: [magnets],
        NEW_TEXT_FIELDS[2]: [funding_source],
        NEW_TEXT_FIELDS[3]: [strategy],
        NEW_TEXT_FIELDS[4]: [management_decisions]
    }
    
    return pd.DataFrame.from_dict(data)


def load_default_values() -> dict:
    """
    Загружает последние значения по умолчанию для каждого направления
    
    Returns:
        dict: Словарь вида {direction: {field_name: last_value}}
    """
    if os.path.exists(AUTOCOMPLETE_FILE):
        try:
            with open(AUTOCOMPLETE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    else:
        return {}


def save_default_values(default_values: dict) -> None:
    """
    Сохраняет последние значения по умолчанию для каждого направления
    
    Args:
        default_values: Словарь вида {direction: {field_name: last_value}}
    """
    with open(AUTOCOMPLETE_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_values, f, ensure_ascii=False, indent=2)


def update_default_value(direction: str, field_name: str, value: str) -> None:
    """
    Обновляет последнее значение для конкретного направления и поля
    
    Args:
        direction: Название направления
        field_name: Название поля
        value: Новое значение
    """
    if not value or not value.strip():
        return
    
    default_values = load_default_values()
    
    if direction not in default_values:
        default_values[direction] = {}
    
    default_values[direction][field_name] = value
    
    save_default_values(default_values)


def get_default_value(direction: str, field_name: str) -> str:
    """
    Получает последнее значение для конкретного направления и поля
    
    Args:
        direction: Название направления
        field_name: Название поля
        
    Returns:
        str: Последнее значение или пустая строка
    """
    default_values = load_default_values()
    return default_values.get(direction, {}).get(field_name, "")
