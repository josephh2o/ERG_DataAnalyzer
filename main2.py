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
        fileName = (self.date + "_P01S" + self.session + "T0" + str(i) + "00" 
                    + self.channel + ".csv")
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
        self.fs = 1 / (((np.max(data.ms) - np.min(data.ms)) / 1000.0) 
                       / (np.argmax(data.ms) + 1))
        try:
            self.lpf = float(lpf)
        except ValueError:
            self.lpf = 300.0
        try:
            self.hpf = float(hpf)
        except ValueError:
            self.hpf = 0.3
    
    # Define lpFilter function to pre-process data using Butter low pass
    # filtering
    def lpFilter(self, data):
        sos = signal.butter(1.0, self.lpf, "lowpass", fs = self.fs, 
                            output = "sos")
        data.uV = signal.sosfiltfilt(sos, data.uV)
        return data
    
    # Define hpFilter function to pre-process data using Butter high pass
    # filtering
    def hpFilter(self, data):
        sos = signal.butter(1.0, self.hpf, "highpass", fs = self.fs, 
                            output = "sos")
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
        self.tempms = data.ms[(np.where(data.ms <= 0)[0][-1]): 
                              (np.where(data.ms <= 150)[0][-1])]
        self.tempuV = data.uV[(np.where(data.ms <= 0)[0][-1]): 
                              (np.where(data.ms <= 150)[0][-1])]
        
    # Define flip function to flip the data if recording electrodes were 
    # reversed (NEED TO FIX)
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
    
    # Define plotA1 function to plot dataset
    def plotA1(self, data):
        if (i == 1):
            plt.figure(1)
        plt.plot(data.ms, data.uV, label = "FI " + str(i))
    
    # Define plotA2 function to label plotA1
    def plotA2():
        plt.title("Combined Intensities of Channel " + channel)
        plt.xlabel("Time (ms)")
        plt.ylabel("Voltage (uV)")
        plt.legend(loc = "upper right")
        
    # Define plotB function to plot and label dataset
    def plotB():
        plt.figure(2)
        plt.scatter(dataset, aTime, label = "A Wave")
        plt.plot(dataset, np.poly1d(np.polyfit(dataset, aTime, 1))(dataset))
        plt.scatter(dataset, bTime, label = "B Wave")
        plt.plot(dataset, np.poly1d(np.polyfit(dataset, bTime, 1))(dataset))
        plt.title("Implicit Times of Waveform")
        plt.xlabel("Flash Intensity")
        plt.ylabel("Time (ms)")
        plt.legend(loc = "upper right")
        
    # Define plotC function to plot and label dataset
    def plotC():
        plt.figure(3)
        plt.scatter(dataset, aWave, label = "A Wave")
        plt.plot(dataset, np.poly1d(np.polyfit(dataset, aWave, 1))(dataset))
        plt.scatter(dataset, bWave, label = "B Wave")
        plt.plot(dataset, np.poly1d(np.polyfit(dataset, bWave, 1))(dataset))
        plt.title("Intensities of Waveform")
        plt.xlabel("Flash Intensity")
        plt.ylabel("Voltage (uV)")
        plt.legend(loc = "upper right")

        
    # Define overview function to create a report based on data in console
    def overview(self):
        j = 0
        while j < len(aWave):
            print("Flash Intensity " + str(dataset[j]) + ":\nA Wave: "
                  + str(aWave[j]) + "uV @ " + str(aTime[j]) + "ms\nB Wave: " 
                  + str(bWave[j]) + "uV @ " + str(bTime[j]) + "ms\n")
            j += 1
    
    # Define summary function to create a report based on data in csv
    def summary(self, settings):
        location = "results/"
        csvFileName = date + "_P01S" + session + channel + "_SUMMARY.csv"
        with open(location + csvFileName, "w", newline = "") as csvfile:
            filewriter = csv.writer(csvfile, delimiter = ",")
            filewriter.writerow(["A Wave Amplitude (uV)", 
                                 "B Wave Amplitude (uV)", "B/A Ratio", 
                                 "A/A0 Ratio", "B/B0 Ratio", 
                                 "A Wave Implicit Time (uV)", 
                                 "B Wave Implicit Time (uV)"])
            k = 0
            while k < len(aWave):
                filewriter.writerow([str(aWave[k]), str(bWave[k]), 
                                     str(bWave[k]/ aWave[k]), 
                                     str(aWave[k]/ aWave[0]), 
                                     str(bWave[k]/ bWave[0]),  
                                     str(aTime[k]), str(bTime[k])])
                k += 1
                
            # Write settings in file
            filewriter.writerow("")
            filewriter.writerow(["Settings"])
            filewriter.writerow(["Sampling Frequency (Hz)", settings.fs])
            filewriter.writerow(["Low Pass Filter (Hz)", settings.lpf])
            filewriter.writerow(["High Pass Filter (Hz)", + settings.hpf])
             
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
    data = analysis(liveData)
    analysis.flip(data, liveData)
    analysis.collect(data)
    analysis.plotA1(data, liveData)
    i += 1
analysis.plotA2()
analysis.plotB()
analysis.plotC()
analysis.summary(data, settings)
print("\n------------------DATA------------------")
analysis.overview(data)
print("----------------SETTINGS----------------")
print("Sampling Frequency: " + str(settings.fs) + "Hz\nLow Pass Filter: " 
      + str(settings.lpf) + "Hz\nHigh Pass Filter: " 
      + str(settings.hpf) + "Hz")