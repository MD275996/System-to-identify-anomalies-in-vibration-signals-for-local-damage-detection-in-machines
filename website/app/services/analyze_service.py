# draw spectrogram
import scipy.signal
import numpy as np
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import os
import pandas as pd
import app.services.ifb_selectors as selector

PLOT_FOLDER = "app/static/tmp"
READ_PATH = "static/tmp"
UPLOAD_FOLDER = "app/uploads"

def process_file(signal):
    fs = len(signal)
    array_freq, array_tt, matrix_Zxx = scipy.signal.stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)

    output_paths = []
    output_name = "temp_spec.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    plt.figure(figsize=(18, 6))
    plt.pcolormesh(array_freq, array_tt, 10*np.log10(Zxx.T), shading='gouraud', cmap='plasma')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Czas [s]')
    plt.title('Spektrogram')
    plt.colorbar(label='Amplituda [dB]')
    plt.savefig(output_path)
    plt.close()
    output_paths.append(f"/static/tmp/temp_spec.png")
    #wyrysowanie wykresów
    results_list = [
    ("SK", selector.SK(Zxx)),
    ("JB", selector.JB(Zxx)),
    ("KSS", selector.KSS(Zxx)),
    ("AD", selector.AD(Zxx)),
    ("CVM", selector.CVM(Zxx)),
    ("CVS", selector.CVS(Zxx))
    ]
    colors = [
        "red",
        "blue",
        "green",
        "orange",
        "purple",
        "brown"
    ]

    bands = []
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    axes = axes.ravel()

    for (title, results), color in zip(results_list, colors):
        output_name = f"temp_{title}.png"
        plt.figure(figsize=(18, 6))
        plt.plot(array_freq, results,color=color)
        plt.title(f"Wyniki selektora: {title}")
        plt.xlabel("Częstotliwość")
        plt.ylabel("Wartość selektora")
        plt.grid()
        output_path = os.path.join(PLOT_FOLDER, output_name)
        output_paths.append(output_path[3:])
        plt.savefig(output_path)
        plt.close()

        left,right = detect_impulse_band(array_freq, results)
        bands.append([left,right])
        
    bands = np.array(bands)
    lefts = np.delete(bands[:,0],np.argwhere(bands[:,0] == None))
    rights = np.delete(bands[:,1],np.argwhere(bands[:,1] == None))

    left = np.median(lefts)
    right = np.median(rights)
    boundaries = (left,right)

    return output_paths, boundaries

def get_signal_from_file(filename):
    df = pd.read_csv(f"app/uploads/{filename}", header = None)
    signal = df[0].to_numpy()
    return signal

def draw_signal(signal,filename):
    output_name = filename.replace(".csv",".png")
    output_path = os.path.join(PLOT_FOLDER, output_name)
    plt.figure(figsize=(10, 4))
    plt.plot(signal, linewidth=1)
    plt.title(f"Sygnał w czasie")
    plt.xlabel("Próbka")
    plt.ylabel("Amplituda")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path[3:]

def draw_selector(signal,selektor,output_path):

    results = selektor(signal)

    plt.figure(figsize=(18, 6))
    plt.plot(results)
    plt.title("Wyniki selektora")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    plt.savefig(output_path)
    plt.close()

def detect_impulse_band(freqs, selector_values, k=4, smooth_window=5):
    """
    freqs             - array częstotliwości
    selector_values   - wartości selektora
    k                 - czułość (3-6)
    smooth_window     - wygładzanie

    Zwraca: (f_start, f_end) albo None
    """
    x = np.asarray(selector_values)
    # Wygładzenie za pomocą moving average
    x_smooth = np.convolve(
        x, 
        np.ones(smooth_window)/smooth_window, 
        mode='same'
    )
    # Estymacja tła (odporna na outlier)
    median = np.median(x_smooth)
    mad = np.median(np.abs(x_smooth - median))  # odporna sigma
    if mad == 0:
        return None, None
    z = np.abs(x_smooth - median) / mad
    # Maska anomalii
    anomaly_mask = z > k
    if not np.any(anomaly_mask):
        return None, None
    # Grupowanie w pasma
    idx = np.where(anomaly_mask)[0]
    splits = np.where(np.diff(idx) > 1)[0]
    groups = np.split(idx, splits + 1)
    # Wybór najsilniejszego pasma
    best_group = max(groups, key=len)
    f_start = freqs[best_group[0]]
    f_end   = freqs[best_group[-1]]
    return np.round(f_start), np.round(f_end)

def bandpass_filter(signal, fs, f_low, f_high):
    # Wykonanie FFT
    fft_signal = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1/fs)
    
    # Tworzenie maski dla wybranego pasma
    mask = (abs(freqs) >= f_low) & (abs(freqs) <= f_high)
    
    # Aplikacja maski (wyzerowanie składowych poza wybranym pasmem)
    fft_signal_filtered = fft_signal.copy()
    fft_signal_filtered[~mask] = 0
    
    # Odwrotna transformata Fouriera
    filtered_signal = np.real(np.fft.ifft(fft_signal_filtered))
    
    return filtered_signal, freqs, fft_signal, fft_signal_filtered

def impuls_detection(filtered,impuls_threshold=3):
    filtered = np.abs(filtered)
    filtered_energy  = np.mean(filtered**2)

    if filtered_energy == 0 or np.isnan(filtered_energy):
        return 0.0

    threshold = np.mean(filtered) + impuls_threshold*np.std(filtered)

    filtered_impulses = np.maximum(filtered - threshold, 0)
    filtered_impulses_energy = np.mean(filtered_impulses**2)

    return filtered_impulses_energy/filtered_energy