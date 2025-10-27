from flask import Flask, request, render_template, redirect, url_for
import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

#ta linijka upewnia się że nasz folder istnieje
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok = True)

@app.route("/")         # dekorator, mówi Flaskowi pod jakim adresem URL ma być dostępna ta funkcja
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
    return render_template("generate.html")

@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/analyze", methods = ["POST"])
def analyze():
    #wczytanie pliku
    uploaded_file = request.files["datafile"]
    if uploaded_file.filename == "":
        return redirect(url_for("index"))
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(filepath)

    # Analiza danych (kontynuacja przykładu, później zamienić)
    df = pd.read_csv(filepath, header=None)
    signal = np.array(df[0])
    
    fs = 25000
    array_freq, array_tt, matrix_Zxx = scipy.signal.stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)


    # Tworzenie wykresu
    plt.figure(figsize=(18, 6))
    plt.pcolormesh(array_freq, array_tt, 10*np.log10(Zxx.T), shading='gouraud', cmap='plasma')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Czas [s]')
    plt.title('Spektrogram')
    plt.colorbar(label='Amplituda [dB]')
    plot_path = os.path.join("static", "plot.png")
    os.makedirs("static", exist_ok=True)
    plt.savefig(plot_path)
    plt.close()
        
    return render_template("summary.html", plot_url=plot_path)

if __name__ == "__main__":
    app.run(debug=True)