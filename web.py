import time
from flask import Flask, render_template, jsonify, request
from threading import Thread, Event
from werkzeug.serving import make_server
import webbrowser

from settings.save_data import save_data
from settings.constant import get_data
from settings.logger import get_logger


settings_data = get_data()
module_data_path = "module.json"


class Web:

    def __init__(self, import_name, signals, config_object=None) -> None:
        self.logger = get_logger()
        self.signals = signals
        self.logger.info("Web start init")
        self.app_run = False
        self.app = Flask(import_name, template_folder="templates")
        if config_object:
            self.configure_app(config_object)
        self.setup_route()
        self.server = None
        self.server_thread = None
        self.module_data = get_data(module_data_path)
        self.current_settings = self.module_data["Modules"]["Settings"]

        self.logger.info("Web stop init")

    def configure_app(self, config_object) -> None:
        self.logger.debug("Web start configure app")
        if isinstance(config_object, dict):
            self.app.config.update(config_object)
        else:
            self.app.config.from_object(config_object)
        self.logger.debug("Web stop configure app")

    def add_route(self, route, view_func, methods: list | None = None) -> None:
        self.logger.debug(
            "Web add rout %s with methods [%s] and view function %s",
            route,
            methods,
            view_func,
        )
        if methods is None:
            methods = ["GET"]
        self.app.route(route, methods=methods)(view_func)
        self.logger.debug("Web added rout")

    def run(
        self,
        host=settings_data["Web"]["Host"],
        port=settings_data["Web"]["Port"],
    ) -> None:
        print(r"http://%s:%s" % (host, port))
        self.app_run = True
        self.logger.info("Web start run")

        # Создаем сервер в отдельном потоке
        self.server = make_server(host, port, self.app)
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.start()

        webbrowser.open("http://%s:%s" % (host, port))

        # Основной цикл проверки сигнала завершения
        while not self.signals.terminate:
            time.sleep(1)

        # Завершаем работу Flask-приложения
        self.logger.info("Web stopping...")
        self.server.shutdown()  # Останавливаем сервер
        self.server_thread.join()
        self.logger.info("Web stopped")

    def get_last_logs(self) -> str:
        return "\n".join(self.logger.handlers[1].get_last_messages)

    def _save_data(self, new_data) -> None:
        wwd = new_data["WWD"]
        stt = new_data["STT"]
        tts = new_data["TTS"]
        llm = new_data["LLM"]
        save_data(r"module.json", ["Modules", "Settings", 0, "value"], wwd)
        save_data(r"module.json", ["Modules", "Settings", 1, "value"], tts)
        save_data(
            r"module.json",
            [
                "Modules",
                "Settings",
                2,
                "value",
            ],
            llm,
        )
        save_data(r"module.json", ["Modules", "Settings", 3, "value"], stt)

        self.current_settings = self.module_data["Modules"]["Settings"]
        print(self.current_settings)
        print(new_data)

    def setup_route(self) -> None:

        @self.app.route("/update-info")
        def update_info():
            return jsonify(
                {
                    "message": self.get_last_logs(),
                }
            )

        @self.app.route("/")
        def home():
            return render_template(
                template_name_or_list="home.html",
                title="Главная страница",
                message="Добро пожаловать!",
            )

        @self.app.route("/logs")
        def logs():
            return render_template(
                template_name_or_list="logs.html",
                title="Логи",
            )

        @self.app.route("/settings")
        def settings():
            return render_template(
                template_name_or_list="settings.html",
                title="Настройки",
            )

        @self.app.route("/start", methods=["POST"])
        def start():
            self.signals.neuro_run = True
            return jsonify({"status": "success", "message": "Запущено"})

        @self.app.route("/stop", methods=["POST"])
        def stop():
            self.signals.neuro_run = False
            return jsonify({"status": "success", "message": "Остановлено"})

        @self.app.route("/shutdown", methods=["POST"])
        def shutdown():
            self.signals.terminate = True
            return jsonify({"status": "success", "message": "Выключение"})

        @self.app.route("/status")
        def status():
            return jsonify(
                {
                    "isRunning": self.signals.neuro_run,
                }
            )

        @self.app.route("/api/settings", methods=["GET"])
        def get_settings():
            return jsonify(self.current_settings)

        @self.app.route("/api/settings", methods=["POST"])
        def save_settings():
            self.logger.info("Web start save settings")
            new_settings = request.json
            self._save_data(new_settings)
            self.logger.info("Web stop save settings")
            return jsonify({"status": "success"})
