import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

headers = ["ms", "uV"]
file = pd.read_csv("220810_P01S01T0700A.csv", names = headers)
plt.plot(file.ms, file.uV, label = "no filter")

noise = 60
cutoff = 300
fs = 1 / (((np.max(file.ms) - np.min(file.ms)) / 1000) / (np.argmax(file.ms) + 1))

#bNotch, aNotch = signal.iirnotch(.5, .55)
bNotch, aNotch = signal.iirdesign(59, 61, 2, 3, fs = fs)
file.uV = signal.filtfilt(bNotch, aNotch, file.uV)

plt.plot(file.ms, file.uV, label = "filtered")

bNotch, aNotch = signal.butter(1, cutoff, btype = "low", fs = fs)
file.uV = signal.filtfilt(bNotch, aNotch, file.uV)
plt.plot(file.ms, file.uV, label = "filtered2")

plt.legend(loc = "upper right")
plt.show()