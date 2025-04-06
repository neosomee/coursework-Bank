import pandas as pd

def xlsx_reader(file_path: str) -> list:
    """
    Функция для получения данных из xls файла.
    """
    try:
        data = pd.read_excel(file_path)
        if not data.empty and "Номер карты" in data.columns:
            data["Номер карты"] = data["Номер карты"].astype(str)
        return data.to_dict("records")
    except FileNotFoundError:
        return []