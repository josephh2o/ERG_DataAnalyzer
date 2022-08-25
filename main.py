import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
import sys

# Default
dataset = []
aWave = []
bWave = []
aTime = []
bTime = []

# User Input
print("\n---------------INITIALIZE---------------")
date = input("Enter date (yymmdd): ")
sessionNumber = input("Session Number (##): ")
channel = input("Channel(X): ")
lpf = input("Enter Low Pass Frequency (Default 300Hz): ")
if lpf == "":
    lpf = 300.0
else:
    float(lpf)
hpf = input("Enter High Pass Frequency (Default 0.3Hz): ")
if hpf == "":
    hpf = 0.3
else:
    float(hpf)

# Main
print("\n---------------FILES READ---------------")
i = 1;
plt.figure(1)
while i > 0:
    location = "data/"
    fileName = date + "_P01S" + sessionNumber + "T0" + str(i) + "00" + channel + ".csv"
    headers = ["ms", "uV"]
    try:
        file = pd.read_csv(location + fileName, names = headers)
    except FileNotFoundError:
        if (i == 1):
            print("File(s) not found.")
            sys.exit("")
        break
    
    # Pre-Processing, Low Pass Filtering
    fs = 1 / (((np.max(file.ms) - np.min(file.ms)) / 1000.0) / (np.argmax(file.ms) + 1))
    sos = signal.butter(1.0, lpf, "lowpass", fs = fs, output = "sos")
    file.uV = signal.sosfiltfilt(sos, file.uV)
    
    # Pre-Processing, High Pass Filtering
    sos = signal.butter(1.0, hpf, "highpass", fs = fs, output = "sos")
    file.uV = signal.sosfiltfilt(sos, file.uV)
    
    # Pre-Processing, 60 hz Filtering
    # bNotch, aNotch = signal.iirnotch(60.0, 1.0, fs = fs)
    # file.uV = signal.filtfilt(bNotch, aNotch, file.uV)
    
    # Pre-Processing, Normalize
    normDiff = np.mean(file.uV[0: np.where(file.ms <= 0)[0][-1]])
    file.uV = file.uV - normDiff
    
    # Flip Data
    tempms = file.ms[(np.where(file.ms <= 0)[0][-1]): (np.where(file.ms <= 150)[0][-1])]
    tempuV = file.uV[(np.where(file.ms <= 0)[0][-1]): (np.where(file.ms <= 150)[0][-1])]
    if np.argmax(tempuV) > np.argmin(tempuV):
        file.uV = file.uV
        
    elif np.argmax(tempuV) < np.argmin(tempuV):
        file.uV = 0 - file.uV
    
    # Wave Data Collection
    dataset.append(i)
    aWave.append(0 - np.min(tempuV))
    bWave.append(np.max(tempuV) - np.min(tempuV))
    aTime.append(tempms.values[np.argmin(tempuV)])
    bTime.append(tempms.values[np.argmax(tempuV)])
    
    # Plotting per Dataset
    plt.plot(file.ms, file.uV, label = "FI " + str(i))
    print(fileName)
    i += 1

# Data
print("\n------------------DATA------------------")
k = 0
while k < len(aWave):
    print("Flash Intensity " + str(dataset[k]) + ":\nA Wave: "+ str(aWave[k]) + "uV @ " + str(aTime[k]) + "ms\nB Wave: " + str(bWave[k]) + "uV @ " + str(bTime[k]) + "ms\n")
    k += 1

# Data to CSV
csvFileName = date + "_P01S" + sessionNumber + channel + "_SUMMARY.csv"
with open(csvFileName, "w", newline = "") as csvfile:
    filewriter = csv.writer(csvfile, delimiter = ",")
    filewriter.writerow(["A Wave Amplitude (uV)", "B Wave Amplitude (uV)", "B/A Ratio", "A/A0 Ratio", "B/B0 Ratio", "A Wave Implicit Time (uV)", "B Wave Implicit Time (uV)"])
    l = 0
    while l < len(aWave):
        filewriter.writerow([str(aWave[l]), str(bWave[l]), str(bWave[l]/ aWave[l]), str(aWave[l]/ aWave[0]), str(bWave[l]/ bWave[0]),  str(aTime[l]), str(bTime[l])])
        l += 1


# Diagnostics
print("----------------SETTINGS----------------")
print("Sampling Frequency: " + str(fs) + "Hz\nLow Pass Filter: " + str(lpf) + "Hz\nHigh Pass Filter: " + str(hpf) + "Hz")

# Plot Data
plt.title("Combined Intensities of Channel " + channel)
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (uV)")
plt.legend(loc = "upper right")

plt.figure(2)
plt.scatter(dataset, aTime, label = "A Wave")
plt.plot(dataset, np.poly1d(np.polyfit(dataset, aTime, 1))(dataset))
plt.scatter(dataset, bTime, label = "B Wave")
plt.plot(dataset, np.poly1d(np.polyfit(dataset, bTime, 1))(dataset))
plt.title("Implicit Times of Waveform")
plt.xlabel("Flash Intensity")
plt.ylabel("Time (ms)")
plt.legend(loc = "upper right")

plt.figure(3)
plt.scatter(dataset, aWave, label = "A Wave")
plt.plot(dataset, np.poly1d(np.polyfit(dataset, aWave, 1))(dataset))
plt.scatter(dataset, bWave, label = "B Wave")
plt.plot(dataset, np.poly1d(np.polyfit(dataset, bWave, 1))(dataset))
plt.title("Intensities of Waveform")
plt.xlabel("Flash Intensity")
plt.ylabel("Voltage (uV)")
plt.legend(loc = "upper right")

plt.show()