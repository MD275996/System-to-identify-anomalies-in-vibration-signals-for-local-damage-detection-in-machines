# draw spectrogram
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt

def draw_spectrogram(signal):
    # STFT
    fs = len(signal)
    array_freq, array_tt, matrix_Zxx = scipy.signal.stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)

    plt.figure(figsize=(18, 6))
    plt.pcolormesh(array_freq, array_tt, 10*np.log10(Zxx.T), shading='gouraud', cmap='plasma')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Czas [s]')
    plt.title('Spektrogram')
    plt.colorbar(label='Amplituda [dB]')
    plt.show()
    
    pass

# draw selectors
def draw_selectors(selectors_data):
    pass