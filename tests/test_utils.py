import pandas as pd
import pytest
import os
from src.utils import xlsx_reader

def test_xlsx_reader(tmp_path):
    """Тест на корректное чтение нормального файла"""
    df = pd.DataFrame({
        "Номер карты": ["1234567890123456", "6543210987654321"],
        "Имя": ["Иван", "Мария"]
    })
    test_file = os.path.join(tmp_path, "test.xlsx")
    df.to_excel(test_file, index=False)

    result = xlsx_reader(test_file)

    assert len(result) == 2
    assert result[0]["Номер карты"] == "1234567890123456"
    assert result[1]["Имя"] == "Мария"


def test_xlsx_reader_card_numbers(tmp_path):
    """Тест на преобразование числовых номеров карт в строки"""
    df = pd.DataFrame({
        "Номер карты": [1234567890123456, 9876543210987654],
        "Имя": ["Алексей", "Ольга"]
    })
    test_file = os.path.join(tmp_path, "testik.xlsx")
    df.to_excel(test_file, index=False)

    result = xlsx_reader(test_file)
    assert result[0]["Номер карты"] == "1234567890123456"
    assert result[1]["Номер карты"] == "9876543210987654"


