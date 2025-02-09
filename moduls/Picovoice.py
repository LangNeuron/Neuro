import pvporcupine
from module_base.wakeworddetection import WakeWordDetector
import struct
from pvrecorder import PvRecorder
from datetime import datetime


class WakeWordDetector(WakeWordDetector):
    def __init__(
        self,
        token="",
        keywords=None,
        sensitivity=0.5,
    ):
        """
        Реализация wake word detector на основе Picovoice Porcupine.
        :param token: Токен не используется, но передается для совместимости
        :param keywords: Список wake word
        :param sensitivity: Чувствительность детекции (0.0 - 1.0)
        """
        if keywords is None:
            keywords = ["jarvis"]
        super().__init__(token)
        self.keywords = keywords
        self.sensitivity = sensitivity

        # Инициализация Porcupine
        self.porcupine = pvporcupine.create(
            access_key=self.token,
            keywords=self.keywords,
            sensitivities=[self.sensitivity] * len(self.keywords),
        )

    def detect(self, audio_data):
        """
        Обрабатывает аудиоданные и проверяет наличие wake word.
        :param audio_data: Фрагмент аудиоданных
        :return: True, если wake word обнаружено, иначе False
        """
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, audio_data)
        keyword_index = self.porcupine.process(pcm)
        return keyword_index >= 0

    def run(self, signals):
        """
        Запускает детекцию wake word в реальном времени.
        """
        recorder = PvRecorder(frame_length=self.porcupine.frame_length)
        recorder.start()

        print("Listening for wake word...")

        try:
            while signals.neuro_run is True:
                pcm = recorder.read()
                result = self.porcupine.process(pcm)

                if result >= 0:
                    print(
                        "[%s] Detected %s"
                        % (str(datetime.now()), self.keywords[result])
                    )
        except KeyboardInterrupt:
            print("Stopping ...")
        finally:
            recorder.delete()
            self.porcupine.delete()
