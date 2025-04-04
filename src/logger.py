import logging


def logging_setup():
    """
    (Функция для настройки логирования).
    """
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler("nyalog.log", "w", encoding="utf8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)
    return logger