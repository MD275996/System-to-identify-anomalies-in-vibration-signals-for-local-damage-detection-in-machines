from flask import Flask

def create_app():
    app = Flask(__name__)

    #import blueprintów
    from app.routes.api.files_api import files_api
    from app.routes.api.load_api import load_api
    from app.routes.api.generate_api import generate_api
    from app.routes.files import files_page
    from app.routes.base import base_page
    from app.routes.load import load_page
    from app.routes.generate import generate_page  

    #rejestracja blueprintów
    app.register_blueprint(files_api)
    app.register_blueprint(load_api)
    app.register_blueprint(generate_api)
    app.register_blueprint(files_page)
    app.register_blueprint(base_page)
    app.register_blueprint(load_page)
    app.register_blueprint(generate_page)
    return app

#po co to robimy?
# flask musi wiedzieć o blueprintach
# api i strony muszą zostać wpięte do aplikacji