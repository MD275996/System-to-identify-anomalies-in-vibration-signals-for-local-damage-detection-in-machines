# draw spectrogram
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import app.services.ifb_selectors as selector

PLOT_FOLDER = "app/static/tmp"

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

    fig, axes = plt.subplots(3,2,figsize=(18,20))
    axes[0,0].plot(array_freq,sk_results,'bo-')
    axes[0,0].set_title("Spectral Kurtosis")
    axes[0,0].set_xlabel("Częstotliwość")
    axes[0,0].set_ylabel("Wartość selektora")

    axes[0,1].plot(array_freq,jb_results,'ro-')
    axes[0,1].set_title("Jarque-Bera")
    axes[0,1].set_xlabel("Częstotliwość")
    axes[0,1].set_ylabel("Wartość selektora")

    axes[1,0].plot(array_freq, kss_results,'go-')
    axes[1,0].set_title("Kolmogorov-Smirnov")
    axes[1,0].set_xlabel("Częstotliwość")
    axes[1,0].set_ylabel("Wartość selektora")

    axes[1,1].plot(array_freq, ad_results,'co-')
    axes[1,1].set_title("Anderson Darling")
    axes[1,1].set_xlabel("Częstotliwość")
    axes[1,1].set_ylabel("Wartość selektora")

    axes[2,0].plot(array_freq, cvm_results,'mo-')
    axes[2,0].set_title("Cramer-von Mises")
    axes[2,0].set_xlabel("Częstotliwość")
    axes[2,0].set_ylabel("Wartość selektora")

    axes[2,1].plot(array_freq, cvs_results,'ko-')
    axes[2,1].set_title("Conditional Variance")
    axes[2,1].set_xlabel("Częstotliwość")
    axes[2,1].set_ylabel("Wartość selektora")

    axes[0,0].grid()
    axes[0,1].grid()
    axes[1,0].grid()
    axes[1,1].grid()
    axes[2,0].grid()
    axes[2,1].grid()

    plt.tight_layout()
    output_name = "temp_selectors.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    plt.savefig(output_path)
    plt.close
    output_paths.append(f"/static/tmp/temp_selectors.png")

    return output_paths