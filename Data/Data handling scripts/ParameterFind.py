import FileHandler as FH
from Plottools import GetParams
import numpy as np

def main():
    files = FH.ChooseFiles() 
    data = {}
    params = []
    for file in files:
        data = FH.ReadJson(file)
        SpectralX = data["SpectralX"]
        for key in data:
            if key != "SpectralX":
                # FWHM, peak, base
                npinput = np.array([SpectralX,data[key]["Data"]])
                print(npinput)
                params = GetParams(np.array([SpectralX,data[key]["Data"]]))
                data[key]["FWHM"] = params[0]
                data[key]["peak"] = params[1]
                data[key]["baseline"] = params[2]
        FH.WriteJson(file, data)
        print(file[file.rfind("/")+1:]+" done")
    
    
if __name__ == "__main__":
    main()