from flask import Flask, request, render_template, redirect, url_for
import os 
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

#ta linijka upewnia się że nasz folder istnieje
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok = True)

@app.route("/")         # dekorator, mówi Flaskowi pod jakim adresem URL ma być dostępna ta funkcja
def index():
    return render_template("index.html")

@app.route("/analyze", methods = ["POST"])
def analyze():
    #wczytanie pliku
    uploaded_file = request.files["datafile"]
    if uploaded_file.filename == "":
        return redirect(url_for("index"))
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(filepath)

    # Analiza danych (kontynuacja przykładu, później zamienić)
    df = pd.read_csv(filepath)
    
    #tu przyjdzie kod
    boolean = 1
    if boolean:
        return render_template("summary.html")

if __name__ == "__main__":
    app.run(debug=True)