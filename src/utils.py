import json
from json import JSONDecodeError
import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)
log_dir = r'C:\Users\Dareshin.D\PycharmProjects\coursework\logs'

file_handler = logging.FileHandler(os.path.join(log_dir, 'utils.log'))
file_formater = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical("Critical message")


def connect_to_json(path):
    if not path.lower().endswith('.json'):
        logger.error(f'Invalid file format: {path}')
        print(f'Invalid file format: {path}')
        return []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.debug(f'Successfully loaded JSON data from {path}')
            return data
    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
        print(f'File not found: {e}')
        return []
    except (JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f'Error reading JSON: {e}')
        print(f'Error reading JSON: {e}')
        return []


def connect_to_excel(path):
    if not path.lower().endswith('.xlsx'):
        logger.error(f'Invalid Excel file format: {path}')
        print(f'Invalid Excel file format: {path}')
        return []

    try:
        data = pd.read_excel(path)
        logger.debug(f'Successfully loaded Excel data from {path}')
        return data.to_dict(orient='records')
    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
        print(f'File not found: {e}')
        return []
    except Exception as e:
        logger.error(f'Error reading Excel: {e}')
        print(f'Error reading Excel: {e}')
        return []


if __name__ == "__main__":
    excel_data = connect_to_excel(r'C:\Users\Dareshin.D\PycharmProjects\coursework\data\operations.xlsx')
    print(excel_data)
