from flask import Blueprint, render_template
#zwykłe przekierowanie nas do odpowiedniej strony html

files_page = Blueprint("files_page", __name__)

@files_page.get("/files")
def files():
    return render_template("files.html")