from flask import Blueprint, render_template
#zwykłe przekierowanie nas do odpowiedniej strony html

base_page = Blueprint("base_page", __name__)

@base_page.get("/")
def base():
    return render_template("base.html")