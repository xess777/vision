from flask import Flask

from api.images.views import api as images_api


class App(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_blueprints()

    def __init_blueprints(self):
        self.register_blueprint(images_api)


def create_app():
    return App('vision')


app = create_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
