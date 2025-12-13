import numpy as np
import scipy

def normalize(x):
    m = np.max(x)
    if m<= 0 or np.isnan(m):
        return x
    return x/m

def SK(Zxx):
    F = Zxx.shape[0]
    T = Zxx.shape[1]

    num = np.sum(Zxx**4, axis=1)
    den = np.sum(Zxx**2, axis=1)
    sk = (T * num / den**2) - 2

    results = normalize(sk)
    if np.mean(results) > 0.5:
        return 1-results
    return results


def JB(Zxx):
    F = Zxx.shape[0]
    T = Zxx.shape[1]
    jb_results = np.zeros(F)

    for f in range(F):
        s = scipy.stats.skew(Zxx[f])    
        k = scipy.stats.kurtosis(Zxx[f], fisher=True)
        jb_results[f] = T/6 * (s**2 + (np.power(k,2)/4))
    

    return normalize(jb_results)

def KSS(Zxx):
    F = Zxx.shape[0]
    T = Zxx.shape[1]
    kss_results = np.zeros(F)
    for f in range(F):
        mean_signal = np.mean(Zxx[f])
        std_signal = np.std(Zxx[f])
        stat = scipy.stats.kstest(
            Zxx[f],
            'norm',
            args=(mean_signal, std_signal)
        ).statistic
        kss_results[f] = 1/stat
    

    return normalize(kss_results)

def AD(Zxx):    
    F = Zxx.shape[0]
    T = Zxx.shape[1]
    ad_results = np.zeros(F)
    for f in range(F):
        ad_results[f] = scipy.stats.anderson(Zxx[f], dist='norm').statistic


    return normalize(ad_results)

def CVM(Zxx):
    F = Zxx.shape[0]
    T = Zxx.shape[1]
    results = np.zeros(F)

    for f in range(F):
        results[f] = scipy.stats.cramervonmises(Zxx[f],cdf="norm").statistic
    results = results/max(results)
    if np.mean(results) > 0.5:
        return 1-results
    return results

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

        N = 1/p * ((np.var(L)-np.var(M))/np.var(Zxx[f])+(np.var(R)-np.var(M))/np.var(Zxx[f])) * np.sqrt(len(Zxx[f]))

        cvs_results[f] = N

    cvs_results = normalize(cvs_results)
    if np.mean(cvs_results) > 0.5:
        return 1-cvs_results
    return cvs_results