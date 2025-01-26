from flask import Flask, render_template, jsonify


from settings.constant import data
from settings.logger import get_logger


class Web:

    def __init__(self, import_name, config_object=None):
        self.logger = get_logger()
        self.logger.info("Web start init")
        self.app = Flask(import_name, template_folder='templates')
        if config_object:
            self.configure_app(config_object)
        self.setup_route()
        self.logger.info("Web stop init")

    def configure_app(self, config_object):
        self.logger.debug("Web start configure app")
        if isinstance(config_object, dict):
            self.app.config.update(config_object)
        else:
            self.app.config.from_object(config_object)
        self.logger.debug("Web stop configure app")

    def add_route(self, route, view_func, methods: list | None = None):
        self.logger.debug(
            "Web add rout %s with methods [%s] and view function %s",
                route, methods, view_func
            )
        if methods is None:
            methods = ['GET']
        self.app.route(route, methods=methods)(view_func)
        self.logger.debug("Web added rout")

    def run(self,
            host=data["Web"]["Host"],
            port=data["Web"]["Port"],
            debug=data["Web"]["Debug"]
    ):
        self.logger.info("Web start run")
        self.app.run(host=host, port=port, debug=debug)


    def get_last_logs(self) -> str:
        return "\n".join(self.logger.handlers[1].get_last_messages)


    def setup_route(self):

        @self.app.route('/update-info')
        def update_info():
            return jsonify({
                "message": self.get_last_logs(),
            })

        @self.app.route('/')
        def home():
            return render_template(
                template_name_or_list="home.html",
                title="Главная страница",
                message="Добро пожаловать!"
            )

        @self.app.route('/logs')
        def about():
            return render_template(
                template_name_or_list="logs.html",
                title="Логи",
            )


web = Web(data["Web"]["Name"], data["Web"]["config_object"])