import logging
from logging.handlers import RotatingFileHandler
from os import mkdir, path


levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def get_logger(name="app", level: str = 'INFO'):
    global levels
    log = logging.getLogger(name)
    if not log.hasHandlers():  # Проверяем, есть ли уже обработчики
        from settings.constant import data
        if not path.exists('logs'):
            mkdir('logs')
        log.setLevel(levels[level])
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        # Создаем обработчик для записи в файл
        file_handler = RotatingFileHandler(
            r"logs/app.log",
            maxBytes=data["logger"]["MaxBytes"],
            backupCount=data["logger"]["backupCount"],
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        log.addHandler(console_handler)
    return log