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


    output_name = "temp_sk.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    draw_selector(Zxx, selector.SK, output_path)
    output_paths.append(output_path[3:])

    output_name = "temp_jb.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    draw_selector(Zxx, selector.JB, output_path)
    output_paths.append(output_path[3:])

    output_name = "temp_kss.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    draw_selector(Zxx, selector.KSS, output_path)
    output_paths.append(output_path[3:])

    output_name = "temp_ad.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    draw_selector(Zxx, selector.AD, output_path)
    output_paths.append(output_path[3:])

    output_name = "temp_cvm.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    draw_selector(Zxx, selector.CVM, output_path)
    output_paths.append(output_path[3:])

    output_name = "temp_cvs.png"
    output_path = os.path.join(PLOT_FOLDER, output_name)
    draw_selector(Zxx, selector.CVS, output_path)
    output_paths.append(output_path[3:])

    return output_paths

def draw_selector(signal,selektor,output_path):

    results = selektor(signal)

    plt.figure(figsize=(18, 6))
    plt.plot(results)
    plt.title("Wyniki selektora")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    plt.savefig(output_path)
    plt.close


def spike_interval_by_peak(data, threshold_factor=2):
    data = np.array(data)
    baseline = np.median(data)
    uplift = np.std(data)
    threshold = baseline + threshold_factor*uplift

    left,right = 0,0
    # 1. Znajdź największy peak powyżej thresholdu
    idx_peak = np.argmax(data)
    if data[idx_peak] < threshold:
        return left, right, threshold  # brak impulsu

    # 2. Rozszerz w lewo
    left = idx_peak
    while left > 0 and data[left] > threshold:
        left -= 1
    # 3. Rozszerz w prawo
    right = idx_peak
    while right < len(data)-1 and data[right] > threshold:
        right += 1

    return left, right, threshold

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

def impuls_detection(filtered,impuls_threshold):
    filtered_energy  = np.sum(filtered**2)
    impulses = (filtered > np.mean(filtered) + impuls_threshold*np.std(filtered)) | (filtered < np.mean(filtered) - impuls_threshold*np.std(filtered))

    filtered_no_impulses = filtered.copy()
    filtered_no_impulses[impulses] = 0
    filtered_no_impulses_energy = np.sum(filtered_no_impulses**2)
    return filtered_no_impulses_energy/filtered_energy

def calculate_analysis(signal, selektor, filter_threshold=1, impuls_threshold=1):
    #spektrogram
    fs = 1
    array_freq, array_tt, matrix_Zxx = scipy.signal.stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)
    
    #selektor
    results = selektor(Zxx)
    
    #odnalezienie granic
    left, right, threshold = spike_interval_by_peak(results,filter_threshold)

    #filtracja na podstawie otrzymanych granic
    filtered, _, _, _ = bandpass_filter(signal, fs, array_freq[left], array_freq[right])
    sigma = np.std(filtered)
    mu = np.mean(filtered)
    upper_threshold_filtered = mu + impuls_threshold*sigma
    lower_threshold_filtered = mu - impuls_threshold*sigma

    filtered_energy  = np.sum(filtered**2)
    impulses = (filtered > upper_threshold_filtered) | (filtered < lower_threshold_filtered)

    filtered_no_impulses = filtered.copy()
    filtered_no_impulses[impulses] = 0
    filtered_no_impulses_energy = np.sum(filtered_no_impulses**2)

    return filtered_no_impulses_energy/filtered_energy

def draw_analysis(signal, selektor, filter_threshold=1, impuls_threshold=1):
    #sygnał w czasie
    plt.figure(figsize=(10, 4))
    plt.plot(signal, linewidth=1)
    plt.title(f"Sygnał w czasie")
    plt.xlabel("Próbka")
    plt.ylabel("Amplituda")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    #spektrogram
    fs = 1
    array_freq, array_tt, matrix_Zxx = scipy.signal.stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)
    plt.figure(figsize=(18, 6))
    plt.pcolormesh(array_freq, array_tt, 10*np.log10(Zxx.T), shading='gouraud', cmap='plasma')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Czas [s]')
    plt.title('Spektrogram')
    plt.colorbar(label='Amplituda [dB]')
    plt.show()

    #selektor
    results = selektor(Zxx)
    left, right, threshold = spike_interval_by_peak(results,filter_threshold)
    #wyrysowanie wykresów
    plt.figure(figsize=(18,5))
    plt.axvline(x=array_freq[left], color = "red", linestyle = "--")
    plt.axvline(x=array_freq[right], color = "red", linestyle = "--")
    plt.axhline(y=threshold, color = "green", linestyle = "--")
    plt.plot(array_freq,results)
    plt.title("Wyniki selektora")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()


    filtered, _, _, _ = bandpass_filter(signal, fs, array_freq[left], array_freq[right])
    plt.figure(figsize=(18,5))
    plt.plot(filtered)
    plt.title("Sygnał po filtracji")
    plt.xlabel("Czas")
    plt.ylabel("Amplituda")
    plt.grid()

def draw_all_selectors(signal):
    #spektrogram
    fs = 1
    array_freq, array_tt, matrix_Zxx = scipy.signal.stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)


    #selektor
    results = selector.SK(Zxx)
    #wyrysowanie wykresów
    plt.figure(figsize=(18,5))
    plt.plot(array_freq,results)
    plt.title("Wyniki selektora")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    results = selector.JB(Zxx)
    #wyrysowanie wykresów
    plt.figure(figsize=(18,5))
    plt.plot(array_freq,results)
    plt.title("Wyniki selektora")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    results = selector.KSS(Zxx)
    #wyrysowanie wykresów
    plt.figure(figsize=(18,5))
    plt.plot(array_freq,results)
    plt.title("Wyniki selektora")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    results = selector.AD(Zxx)
    #wyrysowanie wykresów
    plt.figure(figsize=(18,5))
    plt.plot(array_freq,results)
    plt.title("Wyniki selektora")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    results = selector.CVM(Zxx)
    #wyrysowanie wykresów
    plt.figure(figsize=(18,5))
    plt.plot(array_freq,results)
    plt.title("Wyniki selektora")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()
    results = selector.CVS(Zxx)
    #wyrysowanie wykresów
    plt.figure(figsize=(18,5))
    plt.plot(array_freq,results)
    plt.title("Wyniki selektora")
    plt.xlabel("Częstotliwość")
    plt.ylabel("Wartość selektora")
    plt.grid()