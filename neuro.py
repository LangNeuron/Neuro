from settings.logger import get_logger
import time
from module_base.wakeworddetection import WakeWordDetector

config_path = "settings/module.json"


class Neuro:
    def __init__(self, signals):
        self.logger = get_logger()
        self.signals = signals

    def run(self):
        detector = WakeWordDetector.from_config(config_path)
        while self.signals.terminate is False:
            while self.signals.neuro_run is True and self.signals.terminate is False:
                detector.run(self.signals)
            time.sleep(1)
        self.logger.info("neuro stop")
