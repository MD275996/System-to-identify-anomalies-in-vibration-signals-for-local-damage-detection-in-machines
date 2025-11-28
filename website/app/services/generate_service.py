import numpy as np
from scipy.signal import firwin, lfilter
import os

def impsim(fs, nx, fmod, amp_imp, f_center, bandwidth):
    """
        fs - częstotliwość próbkowania
        nx - liczba próbek w sygnale wynikowym
        fmod - częstotliwość powtarzania impulsów (lub lista dla wielu)
        amp_imp - amplituda impulsów
        f_center - środkowa częstotliwość pasma
        bandwidth - szerokość pasma wokół f_center
        shift - przesunięcie fazowe sygnału
    """
    #konwersja parametrów do tablic w przypadku jednej wartości
    fmod = np.atleast_1d(fmod)
    amp_imp = np.atleast_1d(amp_imp)
    f_center = np.atleast_1d(f_center)
    bandwidth = np.atleast_1d(bandwidth)

    shift = [0] #zamienić jeśli będziemy chcieli zaimplementować shift
    # shift = np.atleast_1d(shift)
    
    # funkcja pomocnicza impulsu tłumionego 
    def fnx(x, fn, dn):
        return np.sin(2 * np.pi * fn * x) * np.exp(-dn * x)

    # czas trwania pojedyńczego impulsu (50 ms)
    tp = np.arange(0, 0.05, 1/fs )
    pnx = len(tp)

    #wektor czasu całego sygnału
    t = np.arange(1,nx)/fs
    yy = np.zeros(nx)
    
    #główna pętla - dla każdego uszkodzenia
    for j in range(len(fmod)): 
        #projektowanie filtru pasmowego FIR
        low = (f_center[j]-bandwidth[j]) / (fs/2)
        high = (f_center[j]+bandwidth[j]) / (fs/2)
        bp_filt = firwin(numtaps=81, cutoff = [low,high], pass_zero=False)

        syg_c = np.zeros(nx)

        #odległość między impulsami (w próbkach)
        fault_samples = int(round(fs/fmod[j]))

        #pozycje impulsów
        imp_pos = np.arange(0, nx, fault_samples)
        imp_pos = imp_pos[imp_pos + pnx + 1 < len(t)]

        #generowanie impulsów
        for pos in imp_pos:
            y = amp_imp[j] * fnx(tp, f_center[j], 3000)
            syg_c[pos:pos+pnx] += y[:min(pnx, len(syg_c)-pos)]
        
        #Filtracja i przesunięcie
        filtered = lfilter(bp_filt, 1.0, syg_c)
        shifted = np.roll(filtered, int(shift[j]))

        #Dodanie do wyniku
        yy += shifted

    return yy

def gen_signal(B=20, fs=25000, varsize=25000, fmod=30, f_center=5000, bandwidth=1500, sigma = 1):
    """Parametry sygnału
    B:int - amplituda impulsów
    fs:int - częstotliwość próbkowania [Hz]
    varsize:int - długość sygnału = 1 sekunda (domyślnie równe fs)
    
    Parametry impulsów
    fmod:int - częstotliwość powtarzania impulsów [Hz]
    f_center:int - środek pasma [Hz]
    bandwidth:int - szerokość pasma [Hz]
    shift:int - przesunięcie impulsów
    """

    # Generowanie sygnału impulsowego
    y = B * impsim(fs, varsize, fmod, 1, f_center, bandwidth)

    # Dodawanie szumu Gaussa
    sigma = 1
    noise = np.random.normal(0,sigma,varsize)

    # Sygnał końcowy
    signal = noise + y
    return signal

def save_to_file(signal,filename):
    # dostaje sygnał
    # sprawdza jakie pliki są już w folderze 
    # dodaje kolejny wygenerowany plik
    UPLOAD_FOLDER = "app/uploads"
    np.savetxt(os.path.join(UPLOAD_FOLDER, filename), signal,)