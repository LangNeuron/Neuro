import json
import importlib
from abc import ABC, abstractmethod


class WakeWordDetector(ABC):
    def __init__(self, token=None):
        """
        Базовый класс для детекции wake word.
        :param token: Токен для API, если необходим.
        """
        self.token = token

    @abstractmethod
    def detect(self, audio_data):
        """
        Метод для детекции wake word.
        :param audio_data: Входные аудиоданные
        :return: True, если wake word обнаружено, иначе False
        """
        pass

    @abstractmethod
    def run(self, signals):
        """
        Запускает детекцию wake word в реальном времени.
        :param signals: Сигналы для детекции wake word (используется для
        организации проверки работы системы (агента))
        """
        pass

    @staticmethod
    def from_config(config_path):
        """
        Создает экземпляр детектора на основе JSON-конфига.
        :param config_path: Путь к JSON-файлу с конфигурацией
        :return: Экземпляр класса WakeWordDetector
        """
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        module_name: str = config["Modules"]["Settings"][0][
            "value"
        ]  # Имя модуля (без .py)
        params = config["Modules"]["Settings"][0].get("params", {})

        # Динамическая загрузка модуля
        module = importlib.import_module(f"moduls.{module_name}")

        # Получаем класс из модуля (он всегда должен называться WakeWordDetector)
        detector_class = getattr(module, "WakeWordDetector")

        return detector_class(**params)
