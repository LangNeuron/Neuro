from settings.logger import get_logger
from settings.constant import data
import time


class Neuro:
    def __init__(self, signals):
        self.logger = get_logger()
        self.signals = signals

    def run(self):
        while self.signals.terminate is False:
            while self.signals.neuro_run is True and self.signals.terminate is False:
                self.logger.info("neuro run")
                time.sleep(2)
            time.sleep(1)
        self.logger.info("neuro stop")
