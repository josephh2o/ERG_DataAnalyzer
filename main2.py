import csv
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

# Class file
class file:
    
    # Define __init__ function to set user inputs
    def __init__(self):
        self.date = date
        self.session = session
        self.channel = channel
    
    # Define get() function to get, read and store files
    def get(self):
        location = "data/"
        fileName = self.date + "_P01S" + self.session + "T0" + str(i) + "00" + self.channel + ".csv"
        headers = ["ms", "uV"]
        try:
            data = pd.read_csv(location + fileName, names = headers)
            return data
        except FileNotFoundError:
            if (i == 1):
                print("File(s) not found.")
                sys.exit("")
            return None
         
# Class processing    
class processing:
    
    # Define __init__ function to set parameters
    def __init__(self, data):
        self.fs = 1 / (((np.max(data.ms) - np.min(data.ms)) / 1000.0) / (np.argmax(data.ms) + 1))
        if lpf == "":
            self.lpf = 300.0
        else:
            self.lpf = float(lpf)
        if hpf == "":
            self.hpf = 0.3
        else:
            self.hpf = float(hpf)
    
    # Pre-Processing, Low Pass Filtering
    def lpFilter(self, data):
        sos = signal.butter(1.0, self.lpf, "lowpass", fs = self.fs, output = "sos")
        data.uV = signal.sosfiltfilt(sos, data.uV)
        return data
    
    # Pre-Processing, High Pass Filtering
    def hpFilter(self, data):
        sos = signal.butter(1.0, self.hpf, "highpass", fs = self.fs, output = "sos")
        data.uV = signal.sosfiltfilt(sos, data.uV)
        return data
    
    # Pre-Processing, 60 hz Filtering (NOT ISEVC RECOMMENDED)
    def notchFilter(self, data):
        bNotch, aNotch = signal.iirnotch(60.0, 1.0, fs = self.fs)
        data.uV = signal.filtfilt(bNotch, aNotch, data.uV)
        return data
        
    # Pre-Processing, Shifts starting 20ms to 0uV
    def shift(data):
        normDiff = np.mean(data.uV[0: np.where(data.ms <= 0)[0][-1]])
        data.uV = data.uV - normDiff
        return data
    
class analysis:
    
    def __init__(self):
        self.tempms = file.ms[(np.where(file.ms <= 0)[0][-1]): (np.where(file.ms <= 150)[0][-1])]
        self.tempuV = file.uV[(np.where(file.ms <= 0)[0][-1]): (np.where(file.ms <= 150)[0][-1])]
        
    # Flip Data
    def flip(self, data):
        if np.argmax(self.tempuV) > np.argmin(self.tempuV):
            data.uV = data.uV
        elif np.argmax(self.tempuV) < np.argmin(self.tempuV):
            data.uV = 0 - data.uV
        return data
    
    # Wave Data Collection
    def collect(self):
        dataset.append(i)
        aWave.append(0 - np.min(self.tempuV))
        bWave.append(np.max(self.tempuV) - np.min(self.tempuV))
        aTime.append(self.tempms.values[np.argmin(self.tempuV)])
        bTime.append(self.tempms.values[np.argmax(self.tempuV)])
    
    # Define plot function to plot data
    def plot(self, data, i):
        plt.plot(data.ms, data.uV, label = "FI " + str(i))
        
    # Define summary function to create a report based on data
    def summary(self):
        csvFileName = date + "_P01S" + session + channel + "_SUMMARY.csv"
        with open(csvFileName, "w", newline = "") as csvfile:
            filewriter = csv.writer(csvfile, delimiter = ",")
            filewriter.writerow(["A Wave Amplitude (uV)", "B Wave Amplitude (uV)", "B/A Ratio", "A/A0 Ratio", "B/B0 Ratio", "A Wave Implicit Time (uV)", "B Wave Implicit Time (uV)"])
            l = 0
            while l < len(aWave):
                filewriter.writerow([str(aWave[l]), str(bWave[l]), str(bWave[l]/ aWave[l]), str(aWave[l]/ aWave[0]), str(bWave[l]/ bWave[0]),  str(aTime[l]), str(bTime[l])])
                l += 1
        
# Main
print("\n---------------INITIALIZE---------------")
date = input("Enter date (yymmdd): ")
session = input("Session Number (##): ")
channel = input("Channel(X): ")
lpf = input("Enter Low Pass Frequency (Default 300Hz): ")
hpf = input("Enter High Pass Frequency (Default 0.3Hz): ")
dataset1 = file()
i = 1
while i != 0:
    liveData = file.get(dataset1)
    if liveData is None:
        break;
    settings = processing(liveData)
    processing.lpFilter(settings, liveData)
    processing.hpFilter(settings, liveData)
    processing.shift(liveData)
    i += 1