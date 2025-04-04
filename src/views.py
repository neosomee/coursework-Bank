import logging
import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv
import json
import pandas as pd
from src.utils import xlsx_reader

load_dotenv()

API_Cours = os.getenv('API_Cours')
STC_API_KEY = os.getenv('STC_API_KEY')

BASE_DIR = r'C:\Users\Dareshin.D\PycharmProjects\coursework'
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
USER_SETTINGS_PATH = os.path.join(DATA_DIR, 'user_settings.json')
OPERATIONS_XLSX_PATH = os.path.join(DATA_DIR, 'operations.xlsx')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'utils.log'))
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def greetings(actual_time: str) -> str:
    """
    Функция, определяющая приветствие в зависимости от времени суток.
    """
    try:
        logger.debug("Начало обработки времени: %s", actual_time)

        date_obj = datetime.strptime(actual_time, "%H:%M:%S")

        greets = ["Доброй ночи!", "Доброе утро!", "Добрый день!", "Добрый вечер!"]


        if date_obj.hour < 6:
            greet = greets[0]
        elif 6 <= date_obj.hour < 12:
            greet = greets[1]
        elif 12 <= date_obj.hour < 18:
            greet = greets[2]
        else:
            greet = greets[3]

        return greet

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return "Ошибка в обработке времени"

def get_card_info(operations_list: list[dict]) -> list[dict]:
    """
    Функция для сбора информации о картах и операциях.
    """
    card_data = {}
    pattern = re.compile(r"\*\d{4}")

    for operation in operations_list:

        if isinstance(operation["Номер карты"], str) and pattern.fullmatch(operation["Номер карты"]):
            if "Сумма операции" in operation and "Статус" in operation:

                card_number = operation["Номер карты"][1:]
                amount = operation["Сумма операции"]


                if operation["Статус"] == "OK" and float(amount) < 0:
                    if card_number not in card_data:

                        card_data[card_number] = 0.0

                    card_data[card_number] += abs(float(amount))

    result = []


    for card_num, data in card_data.items():
        last_digits = card_num
        total_spent = data
        cashback = total_spent * 0.01

        result.append(
            {"last_digits": last_digits, "total_spent": round(total_spent, 2), "cashback": round(cashback, 2)}
        )

    return result

def get_top_transactions(operations_list: list[dict]) -> list[dict]:
    """
    Функция для определения топ-5 транзакций по сумме.
    """
    n = 5
    result = []

    negative_transactions = [
        operation for operation in operations_list
        if "Сумма операции" in operation and operation["Сумма операции"] < 0
    ]


    top_5 = sorted(negative_transactions, key=lambda x: abs(x["Сумма операции"]), reverse=True)[:n]


    for el in top_5:
        date_str = el["Дата операции"]
        try:
            # Формат с учётом секунд: "%d.%m.%Y %H:%M:%S"
            date_obj = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            amount = abs(el["Сумма операции"])
            category = el["Категория"]
            description = el["Описание"]

            short_info = {
                "date": formatted_date,
                "amount": round(amount, 2),
                "category": category,
                "description": description
            }
            result.append(short_info)
        except ValueError as e:
            logger.error(f"Не удалось преобразовать дату '{date_str}': {e}")
        except KeyError as e:
            logger.error(f"Отсутствует ключ в данных: {e}")

    return result

def get_currency_rates() -> dict:
    """
    Функция для получения актуальных курсов валют.
    """
    rates = {}

    url = "https://open.er-api.com/v6/latest/USD"
    headers = {"apikey": API_Cours}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200 and "rates" in data:
        if "USD" in data["rates"]:
            usd_rate = data["rates"]["RUB"]
            rates["USD"] = round(float(usd_rate), 2)

    url = "https://open.er-api.com/v6/latest/EUR"
    headers = {"apikey": API_Cours}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200 and "rates" in data:
        if "EUR" in data["rates"]:
            euro_rate = data["rates"]["RUB"]
            rates["EUR"] = round(float(euro_rate), 2)

    if not rates:
        logger.error("get_exchange_rates не сработала, rates отсутствуют")
        return {}

    return rates


def get_stocks(stocks_list: list) -> list:
    """
    Функция для получения цен акций.
    """
    user_stocks = []

    for ticker in stocks_list:
        api_url = "https://api.api-ninjas.com/v1/stockprice?ticker={}".format(ticker)
        response = requests.get(api_url, headers={"X-Api-Key": STC_API_KEY})

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, list):
                logger.warning(f"Ответ для акции {ticker} — список. Не удалось получить цену.")
            else:
                price = data.get("price")
                if price is not None:
                    user_stocks.append({"stock": ticker, "price": price})
                else:
                    logger.warning(f"Цена для акции {ticker} не найдена в ответе API")
        else:
            logger.error(f"Ошибка при запросе API для акции {ticker}: {response.status_code}")

    return user_stocks

def main_views():
    """
    Основная функция, запускающая другие.
    """
    data = xlsx_reader(OPERATIONS_XLSX_PATH)

    with open(USER_SETTINGS_PATH, 'r') as f:
        user_data = json.load(f)

    print(f"Текущая дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

    response = process_data(data)
    response_data = json.loads(response)

    print("\nИнформация о карте:")
    for card in response_data["cards"]:
        print(f"Последние цифры карты: {card['last_digits']}")
        print(f"Общая сумма расходов: {card['total_spent']} RUB")
        print(f"Кэшбэк: {card['cashback']} RUB")

    print("\nТоп-5 транзакций:")
    for transaction in response_data["top_transactions"]:
        print(f"Дата: {transaction['date']}")
        print(f"Сумма: {transaction['amount']} RUB")
        print(f"Категория: {transaction['category']}")
        print(f"Описание: {transaction['description']}\n")

    print("\nКурсы валют:")
    for currency, rate in response_data["currency_rates"].items():
        print(f"{currency}: {rate} RUB")

    if "user_stocks" in user_data:
        print("\nАкции пользователя:")
        stock_prices = get_stocks(user_data["user_stocks"])
        for stock in stock_prices:
            print(f"- {stock['stock']}: {stock['price']} USD")
    else:
        print("Ключ 'user_stocks' не найден в JSON файле.")

def process_data(data: list) -> str:
    """
    Основная функция обработки данных.
    """
    greeting = greetings(datetime.now().strftime("%H:%M:%S"))
    cards_data = get_card_info(data)
    top_transactions_data = get_top_transactions(data)
    currency_rates_data = get_currency_rates()

    with open(USER_SETTINGS_PATH, 'r') as f:
        user_settings = json.load(f)

    stock_prices_data = get_stocks(user_settings.get("user_stocks", []))

    response = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions_data,
        "currency_rates": currency_rates_data,
        "stock_prices": stock_prices_data,
    }

    return json.dumps(response, indent=4, ensure_ascii=False)
