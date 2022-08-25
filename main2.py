import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
import sys


dataset = []
aWave = []
bWave = []
aTime = []
bTime = []

class file:
    
    # User input to locate file
    def __init__(self, date, session, channel):
        self.date = date
        self.session = session
        self.channel = channel
    
    # Gets, reads and stores files
    def get(self, i):
        location = "data/"
        fileName = self.date + "_P01S" + self.session + "T0" + str(i) + "00" + self.channel + ".csv"
        headers = ["ms", "uV"]
        try:
            data = pd.read_csv(location + fileName, names = headers)
        except FileNotFoundError:
            if (i == 1):
                print("File(s) not found.")
                sys.exit("")
        return data
            
class processing:
    
    # Define parameters
    def __init__(self):
        self.fs = 1 / (((np.max(file.ms) - np.min(file.ms)) / 1000.0) / (np.argmax(file.ms) + 1))
        lpf = input("Enter Low Pass Frequency (Default 300Hz): ")
        if lpf == "":
            self.lpf = 300.0
        else:
            self.lpf = float(lpf)
        hpf = input("Enter High Pass Frequency (Default 0.3Hz): ")
        if hpf == "":
            self.hpf = 0.3
        else:
            self.hpf = float(hpf)
    
    # Pre-Processing, Low Pass Filtering
    def lpFilter(self):
        sos = signal.butter(1.0, self.lpf, "lowpass", fs = self.fs, output = "sos")
        file.uV = signal.sosfiltfilt(sos, file.uV)
        return file
    
    # Pre-Processing, High Pass Filtering
    def hpFilter(self):
        sos = signal.butter(1.0, self.hpf, "highpass", fs = self.fs, output = "sos")
        file.uV = signal.sosfiltfilt(sos, file.uV)
        return file
    
    # Pre-Processing, 60 hz Filtering (NOT ISEVC RECOMMENDED)
    def notchFilter(self):
        bNotch, aNotch = signal.iirnotch(60.0, 1.0, fs = self.fs)
        file.uV = signal.filtfilt(bNotch, aNotch, file.uV)
        return file
        
    # Pre-Processing, Shifts starting 20ms to 0uV
    def shift():
        normDiff = np.mean(file.uV[0: np.where(file.ms <= 0)[0][-1]])
        file.uV = file.uV - normDiff
        return file
    
class analysis:
    
    def __init__(self):
        tempms = file.ms[(np.where(file.ms <= 0)[0][-1]): (np.where(file.ms <= 150)[0][-1])]
        tempuV = file.uV[(np.where(file.ms <= 0)[0][-1]): (np.where(file.ms <= 150)[0][-1])]
        
    # Flip Data
    def flip(self, file):
        if np.argmax(self.tempuV) > np.argmin(self.tempuV):
            file.uV = file.uV
        elif np.argmax(self.tempuV) < np.argmin(self.tempuV):
            file.uV = 0 - file.uV
        return file
    
    # Wave Data Collection
    def collect(self, i):
        dataset.append(i)
        aWave.append(0 - np.min(self.tempuV))
        bWave.append(np.max(self.tempuV) - np.min(self.tempuV))
        aTime.append(self.tempms.values[np.argmin(self.tempuV)])
        bTime.append(self.tempms.values[np.argmax(self.tempuV)])
    
    # Plotting per Dataset
    def plot(self, file, i):
        plt.plot(file.ms, file.uV, label = "FI " + str(i))
        
# Main
print("\n---------------INITIALIZE---------------")
date = input("Enter date (yymmdd): ")
session = input("Session Number (##): ")
channel = input("Channel(X): ")
init = file(date, session, channel)
i = 1
while i != 0:
    storedData = file.get(init, i)
    print(storedData)
    if storedData == None:
        break
    i += 1

    