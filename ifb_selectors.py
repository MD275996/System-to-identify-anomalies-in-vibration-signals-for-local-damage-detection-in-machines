import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.signal import stft
from scipy.stats import norm

def SK(Zxx):
    F = Zxx.shape[0]
    T = Zxx.shape[1]
    #wyrysować spektrogram
    sk_results = np.zeros(F)

    for f in range(F):
        num = np.sum(np.power(Zxx[f,:],4))
        denum = np.sum(np.power(Zxx[f,:],2))
        sk_results[f] = (T*num/denum) - 2

    return sk_results/max(sk_results)


def JB(Zxx):
    F = Zxx.shape[0]
    T = Zxx.shape[1]
    jb_results = np.zeros(F)

    for f in range(F):
        s = scipy.stats.skew(Zxx[f])    
        k = scipy.stats.kurtosis(Zxx[f])
        jb_results[f] = T/6 * (s**2 + (np.power(k-1,2)/4))
    
    return jb_results/max(jb_results)

def KSS(Zxx):
    F = Zxx.shape[0]
    T = Zxx.shape[1]
    kss_results = np.zeros(F)
    for f in range(F):
        mean_signal = np.mean(Zxx[f])
        std_signal = np.std(Zxx[f])
        cdf_sample = np.zeros(T)
        for i in range(T):
            cdf_sample[i] = scipy.stats.norm.cdf(Zxx[f,i],loc=mean_signal, scale=std_signal)
        test_stats = scipy.stats.kstest(Zxx[f],cdf_sample)
        kss_results[f] = 1/test_stats.statistic
    
    return kss_results/max(kss_results)


def AD(Zxx):    
    F = Zxx.shape[0]
    T = Zxx.shape[1]
    ad_results = np.zeros(F)
    for f in range(F):
        ad_results[f] = scipy.stats.anderson(Zxx[f], dist='norm').statistic
    return ad_results/max(ad_results)  

def CVM(Zxx):
    F = Zxx.shape[0]
    T = Zxx.shape[1]
    results = np.zeros(F)

    for f in range(F):
        results[f] = scipy.stats.cramervonmises(Zxx[f],cdf="norm").statistic
    return results/max(results)

def CVS(Zxx,q=0.2,p=1):
    F = Zxx.shape[0]
    T = Zxx.shape[1]

    cvs_results = np.zeros(F)
    for f in range(F):

        sorted_signal = np.sort(Zxx[f])
        lower_threshold = np.quantile(sorted_signal, q)
        upper_threshold = np.quantile(sorted_signal, 1-q)
        L = sorted_signal[sorted_signal <= lower_threshold]
        R = sorted_signal[sorted_signal > upper_threshold]
        M = sorted_signal[(lower_threshold < sorted_signal) & ( sorted_signal<= upper_threshold)]

        N = 1/p * ((np.var(L)-np.var(M))/np.var(Zxx[0])+(np.var(R)-np.var(M))/np.var(Zxx[0])) * np.sqrt(len(Zxx[f]))

        cvs_results[f] = N

    return cvs_results/max(cvs_results)