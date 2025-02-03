import logging
from logging.handlers import RotatingFileHandler
from os import mkdir, path
from collections import deque

levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class LoggerHandler(logging.Handler):
    def __init__(self, max_len):
        super().__init__()
        self.max_len = max_len
        self.messages = deque(maxlen=max_len)

    def emit(self, record):
        try:
            formatted_message = self.format(record)
            self.messages.appendleft(formatted_message)
        except Exception:
            self.handleError(record)

    @property
    def get_last_messages(self, n=None) -> list:
        if n is None or n > len(self.messages):
            return list(self.messages)
        return list(self.messages)[:n]


def get_logger(name="app", level: str = "INFO"):
    global levels
    log = logging.getLogger(name)
    if not log.hasHandlers():  # Проверяем, есть ли уже обработчики
        from settings.constant import get_data

        data = get_data()
        if not path.exists("logs"):
            mkdir("logs")
        log.setLevel(levels[level])
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        # Создаем обработчик для записи в файл
        file_handler = RotatingFileHandler(
            rf"logs/{name}.log",
            maxBytes=data["logger"]["MaxBytes"],
            backupCount=data["logger"]["backupCount"],
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        save_messages_handler = LoggerHandler(data["logger"]["MaxLen"])
        save_messages_handler.setFormatter(formatter)
        log.addHandler(save_messages_handler)
        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        log.addHandler(console_handler)
    return log
