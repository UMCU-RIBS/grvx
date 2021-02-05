
def compute_zstat(freq_A, freq_B, aoi=1):
    x_A = freq_A.data[0]
    x_B = freq_B.data[0]

    n_A = x_A.shape[aoi]
    n_B = x_B.shape[aoi]
    m = (mean(x_A, axis=aoi) - mean(x_B, axis=aoi))
    Sp = sqrt(var(x_A, axis=aoi, ddof=1) / n_A + var(x_B, axis=aoi, ddof=1) / n_B)
    zstat = m / Sp
    dat = Data(zstat, freq_A.s_freq, chan=freq_A.chan[0], freq=freq_A.freq[0])

    return dat
