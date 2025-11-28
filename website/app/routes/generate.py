from flask import Blueprint, render_template
#zwykłe przekierowanie nas do odpowiedniej strony html

generate_page = Blueprint("generate_page", __name__)

@generate_page.get("/generate")
def generate():
    return render_template("generate.html")