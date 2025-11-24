from flask import Blueprint, render_template
#zwykłe przekierowanie nas do odpowiedniej strony html

analyze_page = Blueprint("analyze_page", __name__)

@analyze_page.get("/analyze")
def analyze():
    return render_template("analyze.html")