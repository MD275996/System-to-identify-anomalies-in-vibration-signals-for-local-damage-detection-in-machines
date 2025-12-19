from flask import Flask
import os
import shutil

TMP_DIR = "app/static/tmp"

def clear_tmp():
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR, exist_ok=True)

def create_app():
    clear_tmp()

    app = Flask(__name__)

    #import blueprintów
    from app.routes.api.files_api import files_api
    from app.routes.api.analyze_api import analyze_api
    from app.routes.api.load_api import load_api
    from app.routes.api.generate_api import generate_api
    from app.routes.files import files_page
    from app.routes.base import base_page
    from app.routes.load import load_page
    from app.routes.generate import generate_page  
    from app.routes.info import info_page  

    #rejestracja blueprintów
    app.register_blueprint(files_api)
    app.register_blueprint(analyze_api)
    app.register_blueprint(load_api)
    app.register_blueprint(generate_api)
    app.register_blueprint(files_page)
    app.register_blueprint(base_page)
    app.register_blueprint(load_page)
    app.register_blueprint(info_page)
    app.register_blueprint(generate_page)
    return app

#po co to robimy?
# flask musi wiedzieć o blueprintach
# api i strony muszą zostać wpięte do aplikacji