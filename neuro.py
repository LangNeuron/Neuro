

from web import web
from settings.logger import get_logger
from settings.constant import data


class Neuro:
    def __init__(self):
        self.web = web

    def run(self):
        self.web.run()

neuro = Neuro()