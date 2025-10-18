import numpy as np
import scipy
from scipy.signal import stft

def SK(signal, fs):
    array_freq, array_tt, matrix_Zxx =stft(signal, fs = 1000, window = 'hann')
    Zxx = np.abs(matrix_Zxx)
    abs_Zxx = np.abs(Zxx)
    num = np.sum(np.power(abs_Zxx[f:],4))
    denum = np.sum(np.power(abs_Zxx[f:],2))
    T = len(t)
    return (T*num/denum)-2 

def JB(Zxx, f, t):
    abs_Zxx = np.abs(Zxx)
    s = scipy.stats.skew(abs_Zxx[f])
    k = scipy.stats.kurtosis(abs_Zxx[f])
    T = len(t)
    print(f"Skewness: {s}, kurtosis: {k}")
    return T/6 * (s**2 + (np.power(k-1,2)/4))

def KSS(Zxx,f,t):
    abs_Zxx = np.abs(Zxx)
    mean_signal = np.mean(abs_Zxx[f])
    std_signal = np.std(abs_Zxx[f])
    cdf_sample = np.zeros_like(t)
    for i in range(len(t)):
        cdf_sample[i] = scipy.stats.norm.cdf(t[i],loc=mean_signal, scale=std_signal)
    return(scipy.stats.kstest(abs_Zxx[f],cdf_sample))