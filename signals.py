from queue import SimpleQueue
from settings.logger import get_logger

class Signals:
    """
    Класс для получения информации о работе какого-то метода
    """
    def __init__(self):
        self.logger = get_logger()
        # очередь для сохранения и выполнения задач
        self.queue = SimpleQueue()

        # Сигнал потокам о завершении работы
        self._terminate = False

        """
        Различная информация о работе приложения,
        для общения между потоками.
        """
        self._last_message_time = 0.0
        self._human_speaking = False
        self._ai_thinking = False
        self._ai_speaking = False
        self._new_message = False
        self._tts_ready = False
        self._stt_ready = False
        self._history = []

    @property
    def last_message_time(self):
        return self._last_message_time

    @last_message_time.setter
    def last_message_time(self, value):
        self._last_message_time = value

    @property
    def human_speaking(self):
        return self._human_speaking

    @human_speaking.setter
    def human_speaking(self, value):
        self._human_speaking = value
        self.queue.put(('human_speaking:', value))
        if value:
            self.logger.info('SIGNALS: Human Talking Start')
        else:
            self.logger.info('SIGNALS: Human Talking Stop')

    @property
    def ai_thinking(self):
        return self._ai_thinking

    @ai_thinking.setter
    def ai_thinking(self, value):
        self._ai_thinking = value
        self.queue.put(('ai_thinking:', value))
        if value:
            self.logger.info('SIGNALS: AI Thinking Start')
        else:
            self.logger.info('SIGNALS: AI Thinking Stop')


    @property
    def ai_speaking(self):
        return self._ai_speaking

    @ai_speaking.setter
    def ai_speaking(self, value):
        self._ai_speaking = value
        self.queue.put(('ai_speaking:', value))
        if value:
            self.logger.info('SIGNALS: AI Speaking Start')
        else:
            self.logger.info('SIGNALS: AI Speaking Stop')

    @property
    def new_message(self):
        return self._new_message

    @new_message.setter
    def new_message(self, value):
        self._new_message = value
        if value:
            self.logger.info('SIGNALS: New Message')

    @property
    def tts_ready(self):
        return self._tts_ready

    @tts_ready.setter
    def tts_ready(self, value):
        self._tts_ready = value

    @property
    def stt_ready(self):
        return self._stt_ready

    @stt_ready.setter
    def stt_ready(self, value):
        self._stt_ready = value

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    @property
    def terminate(self):
        return self._terminate

    @terminate.setter
    def terminate(self, value):
        self._terminate = value
        if value:
            self.logger.info('SIGNALS: Terminate')