from flask import Blueprint, render_template
#zwykłe przekierowanie nas do odpowiedniej strony html

load_page = Blueprint("load_page", __name__)

@load_page.get("/load")
def load():
    return render_template("load.html")