# File type: <Function> return np.ndarray
# By Junxiang H., 2023/07/08
# wacmk.com/cn Tech. Supp.

import numpy as np


def get(ft, unit=1, interval=1, persent=1):
    lf = np.abs(np.fft.fft(ft, n=int(persent * len(ft))))
    fre = np.fft.fftfreq(n=len(lf), d=unit * interval)
    lf = np.fft.fftshift(lf)
    fre = np.fft.fftshift(fre)
    lf = lf[int(len(lf) / 2) :]
    fre = fre[int(len(fre) / 2) :]
    return (fre, lf)


if __name__ == "__main__":
    print("Testing Model:", __file__)
    from matplotlib import pyplot as plt

    t = 0.001 * np.arange(10000)
    lt = np.sin(2 * np.pi * t)
    fre, lf = get(lt)
    plt.plot(fre, lf)
    plt.show()
    print(
        "Testing Result:",
    )  # update here!
