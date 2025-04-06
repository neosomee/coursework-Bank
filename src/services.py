import json
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FILE_PATH = r'C:\Users\neosome\PycharmProjects\coursework-Bank\data\operations.xlsx'

def search_transactions_from_excel(query):
    """
    Поиск транзакций в Excel-файле по описанию или категории.
    """
    try:
        df = pd.read_excel(FILE_PATH)

        query = query.lower()
        result_df = df[
            (df['Описание'].str.contains(query, case=False, na=False)) |
            (df['Категория'].str.contains(query, case=False, na=False))
            ]

        result = result_df.to_dict(orient='records')

        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def main_services():
    """
    Главная функция для поиска транзакций и возврата JSON-ответа.
    """
    query = input("Введите категорию или описание для поиска: ")
    result = search_transactions_from_excel(query)
    print(result)


