import pytest
from unittest.mock import patch, MagicMock
from src.views import (greetings, get_card_info,
                       get_top_transactions, get_currency_rates
                       )


def test_greetings_night():
    assert greetings("02:30:00") == "Доброй ночи!"


def test_greetings_morning():
    assert greetings("08:00:00") == "Доброе утро!"


def test_greetings_afternoon():
    assert greetings("14:00:00") == "Добрый день!"


def test_greetings_evening():
    assert greetings("20:00:00") == "Добрый вечер!"


def test_get_card_info_simple_case():
    test_data = [
        {"Номер карты": "*1234", "Сумма операции": -100, "Статус": "OK"},
        {"Номер карты": "*1234", "Сумма операции": -200, "Статус": "OK"}
    ]
    result = get_card_info(test_data)
    assert len(result) == 1
    assert result[0]["last_digits"] == "1234"
    assert result[0]["total_spent"] == 300.0
    assert result[0]["cashback"] == 3.0


def test_get_top_transactions_simple_case():
    test_data = [
        {"Дата операции": "01.01.2023 12:00:00", "Сумма операции": -500, "Категория": "Еда", "Описание": "Ресторан"},
        {"Дата операции": "01.01.2023 13:00:00", "Сумма операции": -1000, "Категория": "Транспорт", "Описание": "Такси"}
    ]
    result = get_top_transactions(test_data)
    assert len(result) == 2
    assert result[0]["amount"] == 1000
    assert result[1]["category"] == "Еда"


@patch('src.views.requests.get')
def test_get_currency_rates(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 75.5}}
    mock_get.return_value = mock_response

    result = get_currency_rates()
    assert isinstance(result, dict)
