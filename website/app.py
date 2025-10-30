from flask import Flask, request, render_template, redirect, url_for
import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import impuls_simulator as impuls_simulator

app = Flask(__name__)
DATA_FOLDER = "uploads"

#ta linijka upewnia się że nasz folder istnieje
os.makedirs(DATA_FOLDER, exist_ok = True)

@app.route("/")         # dekorator, mówi Flaskowi pod jakim adresem URL ma być dostępna ta funkcja
def home():
    return render_template("home.html")

@app.route('/content/<page>')
def content(page):
    if page == 'analyze':
        return render_template('analyze.html')
    if page == 'load':
        return render_template('load.html')
    elif page == 'generate':
        return render_template('generate.html')
    elif page == 'info':
        return render_template('info.html')
    else:
        return "<p>Nie znaleziono strony.</p>", 404

@app.route("/load_file", methods = ["POST"])
def load_file():
    #wczytanie pliku
    uploaded_file = request.files["datafile"]

    if uploaded_file.filename == "":
        return redirect(url_for("load"))
    
    filepath = os.path.join(DATA_FOLDER, uploaded_file.filename)
    uploaded_file.save(filepath)

        
    return render_template("analyze.html")

@app.route("/analyze")
def analyze_content():
    files = os.listdir(DATA_FOLDER)
    print(files)
    if files:
        return render_template("analyze.html",files = files)
    else :
        return render_template("analyze_empty.html")
# df = pd.read_csv(filepath, header=None)
#     signal = np.array(df[0])
    
#     fs = 25000
#     array_freq, array_tt, matrix_Zxx = scipy.signal.stft(signal, fs = fs, window = 'hann')
#     Zxx = np.abs(matrix_Zxx)


#     # Tworzenie wykresu
#     plt.figure(figsize=(18, 6))
#     plt.pcolormesh(array_freq, array_tt, 10*np.log10(Zxx.T), shading='gouraud', cmap='plasma')
#     plt.xlabel('Częstotliwość [Hz]')
#     plt.ylabel('Czas [s]')
#     plt.title('Spektrogram')
#     plt.colorbar(label='Amplituda [dB]')
#     plot_path = os.path.join("static", "plot.png")
#     os.makedirs("static", exist_ok=True)
#     plt.savefig(plot_path)
#     plt.close()

#     return render_template("summary.html")

@app.route("/generate", methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        # Pobranie danych z formularza
        try:
            # Pobranie danych i konwersja na int
            field1 = int(request.form.get('field1'))
            field2 = int(request.form.get('field2'))
            field3 = int(request.form.get('field3'))
            field4 = int(request.form.get('field4'))
            field5 = int(request.form.get('field5'))
            field6 = int(request.form.get('field6'))
            field7 = int(request.form.get('field7'))
        except (TypeError, ValueError):
            return "Błąd: wszystkie pola muszą być liczbami całkowitymi!", 400

        # Przekazanie danych do funkcji
        signal = impuls_simulator.gen_signal(field1, field2, field3, field4, field5, field6, field7)

        plt.figure(figsize=(10, 4))
        plt.plot(signal, color='blue', linewidth=1)
        plt.title("Sygnał z impulsami i szumem")
        plt.xlabel("Próbka")
        plt.ylabel("Amplituda")
        plt.grid(True)
        plot_path = os.path.join("static", "generated.png")
        os.makedirs("static", exist_ok=True)
        plt.savefig(plot_path)
        plt.close()

        return render_template('info.html', result=signal)
    return render_template("generate.html")

if __name__ == "__main__":
    app.run(debug=True)