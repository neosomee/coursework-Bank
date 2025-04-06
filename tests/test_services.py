import pytest
import pandas as pd
from unittest.mock import patch
import json
from src.services import search_transactions_from_excel

# Тестовые данные
TEST_DATA = [
    {"Описание": "Покупка в магазине", "Категория": "Супермаркет", "Сумма": 1000},
    {"Описание": "Оплата такси", "Категория": "Транспорт", "Сумма": 500},
    {"Описание": "Кафе", "Категория": "Рестораны", "Сумма": 1200}
]

@pytest.fixture
def mock_excel_file(tmp_path):
    """Создаем временный Excel-файл для тестов"""
    test_file = tmp_path / "operations.xlsx"
    df = pd.DataFrame(TEST_DATA)
    df.to_excel(test_file, index=False)
    return test_file

def test_search_transactions_by_description(mock_excel_file):
    """Тест поиска по описанию"""
    with patch('src.services.FILE_PATH', str(mock_excel_file)):
        result = search_transactions_from_excel("такси")
        data = json.loads(result)
        assert len(data) == 1
        assert data[0]["Описание"] == "Оплата такси"

def test_search_transactions_by_category(mock_excel_file):
    """Тест поиска по категории"""
    with patch('src.services.FILE_PATH', str(mock_excel_file)):
        result = search_transactions_from_excel("ресторан")
        data = json.loads(result)
        assert len(data) == 1
        assert data[0]["Категория"] == "Рестораны"

def test_search_transactions_case_insensitive(mock_excel_file):
    """Тест регистронезависимого поиска"""
    with patch('src.services.FILE_PATH', str(mock_excel_file)):
        result = search_transactions_from_excel("МАГАЗИН")
        data = json.loads(result)
        assert len(data) == 1
        assert data[0]["Описание"] == "Покупка в магазине"

