import numpy as np
from GimmePandas import WriteJson
from random import randrange, random
import matplotlib.pyplot as plt

# Generate data files with 10 spectra each,
# 100 points (at baseline except for peak at base-1, 
# left side of peak at base-0.25)
# per spectra, randomly placed 7 points wide peak
# and random baseline between 1 and 2.

def GenerateSpectrum():
    data = []
    peak = randrange(100)
    baseline = random()+1.0
    
    for i in range(100):
        if i < peak-3:
            data.append(baseline-0.25)
        if i > peak-4 and i < peak + 4:
            val = baseline-1+abs(peak-i)*0.2
            data.append(val)
        if i > peak+3:
            data.append(baseline)
    
    return data, peak, baseline

def TestSpectrum():
    data, peak, baseline = GenerateSpectrum()
    print("Peak at "+str(peak)+", baseline: "+str(baseline))
    plt.plot(data)
    plt.show()

def main():
    # TestSpectrum()
    filenumber = 100
    spectraperfile = 10
    
    for i in range(filenumber):
        dict = {}
        filepath = "./testdata/file"+str(i)+".json"
        for j in range(spectraperfile):
            data, peak, baseline = GenerateSpectrum()
            dict2 = {"Data": data, "peak": peak, "baseline": baseline, "Excitation": 200*j}
            dict[str(j)] = dict2
        WriteJson(filepath,dict)
    

if __name__ == "__main__":
    main()
    