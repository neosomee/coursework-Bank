import pytest
import pandas as pd
from src.reports import spending_by_category, read_excel_safe, report_to_file


def test_spending_by_category():
    data = {
        'Дата операции': ['01.01.2024 00:00:00', '15.01.2024 00:00:00', '01.02.2024 00:00:00'],
        'Сумма операции': [-100.0, -200.0, -300.0],
        'Категория': ['Еда', 'Еда', 'Транспорт']
    }
    df = pd.DataFrame(data)

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')

    result = spending_by_category(df, 'Еда', date='01.02.2024')

    assert not result.empty
    assert result.iloc[0]['Категория'] == 'Еда'
    assert result.iloc[0]['Потрачено'] == 300.0

def test_read_excel_safe(tmp_path):
    file_path = tmp_path / "test.xlsx"
    data = {
        'Дата операции': ['01.01.2024 00:00:00'],
        'Сумма операции': [-100.0],
        'Категория': ['Еда']
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

    result = read_excel_safe(file_path)

    assert not result.empty
    assert result.shape == (1, 3)

def test_report_to_file_dir_not_found(tmp_path, capsys):
    @report_to_file("test")
    def test_func():
        return pd.DataFrame({
            'Категория': ['Еда'],
            'Потрачено': [100.0],
            'Период': ['01.01.2024 - 01.01.2024']
        })

    test_func()

    captured = capsys.readouterr()
    assert "Директория logs не найдена" not in captured.out


