import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
import sys

# Create empty variables for storing relevant data
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
    
    # Define lpFilter function to pre-process data using Butter low pass
    # filtering
    def lpFilter(self, data):
        sos = signal.butter(1.0, self.lpf, "lowpass", fs = self.fs, output = "sos")
        data.uV = signal.sosfiltfilt(sos, data.uV)
        return data
    
    # Define hpFilter function to pre-process data using Butter high pass
    # filtering
    def hpFilter(self, data):
        sos = signal.butter(1.0, self.hpf, "highpass", fs = self.fs, output = "sos")
        data.uV = signal.sosfiltfilt(sos, data.uV)
        return data
    
    # Define notchFilter function to pre-process data in which notch filtering 
    # is used to remove 60hz noise(NOT ISEVC RECOMMENDED)
    def notchFilter(self, data):
        bNotch, aNotch = signal.iirnotch(60.0, 1.0, fs = self.fs)
        data.uV = signal.filtfilt(bNotch, aNotch, data.uV)
        return data
        
    # Define shift function to pre-process data in which pre-flash is used to
    # shift data to start at 0
    def shift(data):
        normDiff = np.mean(data.uV[0: np.where(data.ms <= 0)[0][-1]])
        data.uV = data.uV - normDiff
        return data

# Class analysis
class analysis:
    
    # Define __init__ function to create temporary sets of data
    def __init__(self, data):
        self.tempms = file.ms[(np.where(data.ms <= 0)[0][-1]): (np.where(data.ms <= 150)[0][-1])]
        self.tempuV = file.uV[(np.where(data.ms <= 0)[0][-1]): (np.where(data.ms <= 150)[0][-1])]
        
    # Define flip function to flip the data if recording electrodes were 
    # reversed
    def flip(self, data):
        if np.argmax(self.tempuV) > np.argmin(self.tempuV):
            data.uV = data.uV
        elif np.argmax(self.tempuV) < np.argmin(self.tempuV):
            data.uV = 0 - data.uV
        return data
    
    # Define collect function to collect and store wave data
    def collect(self):
        dataset.append(i)
        aWave.append(0 - np.min(self.tempuV))
        bWave.append(np.max(self.tempuV) - np.min(self.tempuV))
        aTime.append(self.tempms.values[np.argmin(self.tempuV)])
        bTime.append(self.tempms.values[np.argmax(self.tempuV)])
    
    # Define plot function to plot data
    def plotA(self, data, i):
        plt.plot(data.ms, data.uV, label = "FI " + str(i))
        
    # Define summary function to create a report based on data
    def summary(self):
        location = "results/"
        csvFileName = date + "_P01S" + session + channel + "_SUMMARY.csv"
        with open(location + csvFileName, "w", newline = "") as csvfile:
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