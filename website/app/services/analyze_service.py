# draw spectrogram
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import app.services.ifb_selectors as selector

PLOT_FOLDER = "app/static/tmp"
READ_PATH = "static/tmp"

def process_file(filename):
    # STFT
    df = pd.read_csv(f"app/uploads/{filename}", header = None)
    signal = df[0].to_numpy()
    # folder na wyniki
    out_dir = os.path.join(PLOT_FOLDER, filename)
    os.makedirs(out_dir, exist_ok=True)

    output_paths = []

    fs = len(signal)
    array_freq, array_tt, matrix_Zxx = scipy.signal.stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)

    plt.figure(figsize=(18, 6))
    plt.pcolormesh(array_freq, array_tt, 10*np.log10(Zxx.T), shading='gouraud', cmap='plasma')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Czas [s]')
    plt.title('Spektrogram')
    plt.colorbar(label='Amplituda [dB]')

    output_name = "temp_spec.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    plt.savefig(output_path)
    plt.close
    output_paths.append(f"/static/tmp/temp_spec.png")

    sk_results = selector.SK(Zxx)
    jb_results = selector.JB(Zxx)
    kss_results = selector.KSS(Zxx)
    ad_results = selector.AD(Zxx)
    cvm_results = 1-selector.CVM(Zxx)
    cvs_results = selector.CVS(Zxx)

    plt.figure(figsize=(18, 6))
    plt.plot(array_freq,sk_results,'bo-')
    plt.title("Spectral Kurtosis")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    output_name = "temp_sk.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    print(output_path)
    output_paths.append(output_path[3:])
    plt.savefig(output_path)
    plt.close

    plt.figure(figsize=(18, 6))
    plt.plot(array_freq,jb_results,'ro-')
    plt.title("Jarque-Bera")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    output_name = "temp_jb.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    output_paths.append(output_path[3:])
    plt.savefig(output_path)
    plt.close

    plt.figure(figsize=(18, 6))
    plt.plot(array_freq, kss_results,'go-')
    plt.title("Kolmogorov-Smirnov")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    output_name = "temp_kss.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    output_paths.append(output_path[3:])
    plt.savefig(output_path)
    plt.close

    plt.figure(figsize=(18, 6))
    plt.plot(array_freq, ad_results,'co-')
    plt.title("Anderson Darling")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    output_name = "temp_ad.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    output_paths.append(output_path[3:])
    plt.savefig(output_path)
    plt.close

    plt.figure(figsize=(18, 6))
    plt.plot(array_freq, cvm_results,'mo-')
    plt.title("Cramer-von Mises")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    output_name = "temp_cvm.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    output_paths.append(output_path[3:])
    plt.savefig(output_path)
    plt.close

    plt.figure(figsize=(18, 6))
    plt.plot(array_freq, cvs_results,'ko-')
    plt.title("Conditional Variance")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    output_name = "temp_cvs.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    output_paths.append(output_path[3:])
    plt.savefig(output_path)
    plt.close



    return output_paths