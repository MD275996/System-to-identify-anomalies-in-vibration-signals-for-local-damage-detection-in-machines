import numpy as np
import scipy
from scipy.signal import stft

def SK(signal, fs):
    array_freq, array_tt, matrix_Zxx =stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)
    
    sk_results = np.zeros_like(array_freq)
    T = len(array_tt)

    for f in range(0,len(array_freq)):
        num = np.sum(np.power(Zxx[f,:],4))
        denum = np.sum(np.power(Zxx[f,:],2))
        sk_results[f] = (T*num/denum) - 2

    return sk_results


def JB(signal, fs):
    array_freq, array_tt, matrix_Zxx =stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)
    T = len(array_tt)
    jb_results = np.zeros_like(array_freq)

    for f in range(len(array_freq)):
        s = scipy.stats.skew(Zxx[f])    
        k = scipy.stats.kurtosis(Zxx[f])
        jb_results[f] = T/6 * (s**2 + (np.power(k-1,2)/4))
    
    return jb_results

def KSS(signal, fs):
    array_freq, array_tt, matrix_Zxx =stft(signal, fs = fs, window = 'hann')
    Zxx = np.abs(matrix_Zxx)
    kss_results = np.zeros_like(array_freq)

    for f in range(len(array_freq)):
        mean_signal = np.mean(Zxx[f])
        std_signal = np.std(Zxx[f])
        cdf_sample = np.zeros_like(array_tt)
        for i in range(len(array_tt)):
            cdf_sample[i] = scipy.stats.norm.cdf(array_tt[i],loc=mean_signal, scale=std_signal)
        test_stats = scipy.stats.kstest(Zxx[f],cdf_sample)
        kss_results[f] = test_stats.pvalue
    return kss_results
