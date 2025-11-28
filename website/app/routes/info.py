from flask import Blueprint, render_template
#zwykłe przekierowanie nas do odpowiedniej strony html

info_page = Blueprint("info_page", __name__)

@info_page.get("/info")
def info():
    return render_template("info.html")