from settings.logger import get_logger


class Signals:
    """
    Класс для получения информации о работе какого-то метода
    """

    def __init__(self):
        self._logger = get_logger()
        self._terminate = False
        self._neuro_run = False

    @property
    def terminate(self):
        return self._terminate

    @terminate.setter
    def terminate(self, value):
        self._logger.info("Terminate set to: %s", value)
        self._terminate = value

    @property
    def neuro_run(self):
        return self._neuro_run

    @neuro_run.setter
    def neuro_run(self, value):
        self._logger.info("Neuro run set to: %s", value)
        self._neuro_run = value
