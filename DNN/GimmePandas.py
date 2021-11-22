import os
import json
import tkinter as tk
import pandas as pd
from tkinter import filedialog

def ChooseFolder(initdir = ".."):
    # Initialise tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Prompt to choose the files to process.
    datafolder = filedialog.askdirectory(initialdir = initdir)
    
    return datafolder

def ChooseFiles(initdir = ".."):
    # Initialise tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Prompt to choose the files to process.
    files = filedialog.askopenfilenames(initialdir = initdir)
    
    # Return filenames as simple list
    return files

def ChooseSingleFile(initdir = ".."):
    # Initialise tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Prompt to choose the files to process.
    file = filedialog.askopenfilename(initialdir = initdir)
    
    # Return filenames as simple list
    return file

def CheckFolder(folderpath):
    # Check whether folder exists, create it if not
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        print("Folder created: " + folderpath)

def WriteJson(filepath, dict):
    # Writes a dictionary to a json file
    folderpath = filepath[:filepath.rfind("/")]
    CheckFolder(folderpath)
    
    with open(filepath, "w") as json_file:  
        json.dump(dict, json_file, indent = 4, sort_keys = True)
    
    return None

def ReadJson(filepath):
    # Reads a json file, returns the dictionary form of the file
    with open(filepath, "r") as json_file:
        dict = json.load(json_file)
    
    return dict

def ReadToPandas(filelist = os.listdir("../Data/TenExSpectra_JSON")):
# simple usage "from GimmePandas import ReadToPandas", call as ReadToPandas()
# You can either manually choose files to read (as argument) or let the function import everything as default
# Reads Json files, returns as pandas dataframe with columns as listed below
    column_names = ["Excitation", "Baseline", "Peak", "FWHM points", "Xdata", "Reflectivity"]
    dataf = pd.DataFrame(columns = column_names, dtype = object)
    dataf
    dataf["Xdata"].astype(object)
    dataf["Reflectivity"].astype(object)
    dataf["FWHM points"].astype(object)
    dftemp = dataf
    
    if filelist == os.listdir("../Data/TenExSpectra_JSON"):
        for i in range(len(filelist)):
            filelist[i] = "../Data/TenExSpectra_JSON/"+filelist[i]
    
    for filepath in filelist:
        dict = ReadJson(filepath)
        X = dict["SpectralX"]
        for key in dict:
            if key != "SpectralX":
                #dftemp = pd.DataFrame({"Excitation": dict[key]["Excitation"], "Xdata": X, "Reflectivity": dict[key]["Data"],\
                #                        "Baseline": dict[key]["baseline"], "Peak": dict[key]["peak"], "FHHM points": dict[key]["FWHM"]},dtype = object)
                dftemp.at[1,"Excitation"] = dict[key]["Excitation"]
                dftemp.at[1,"Xdata"] = X
                dftemp.at[1,"Reflectivity"] = dict[key]["Data"]
                dftemp.at[1,"Baseline"] = dict[key]["baseline"]
                dftemp.at[1,"Peak"] = dict[key]["peak"]
                dftemp.at[1,"FWHM points"] = dict[key]["FWHM"]
                dataf = pd.concat([dataf, dftemp], ignore_index = True)
    print("Dataframe loaded")
    
    return dataf
        
def ReadToPandas2(filelist = os.listdir("../Data/TenExSpectra_JSON")):
# simple usage "from GimmePandas import ReadToPandas", call as ReadToPandas()
# You can either manually choose files to read (as argument) or let the function import everything as default
# Reads Json files, returns as pandas dataframe with columns as listed below
    column_names = ["Excitation", "Baseline", "Peak", "FWHM points", "Xdata", "Reflectivity"]
    dataf = pd.DataFrame(columns = column_names, dtype = object)
    dftemp = dataf
    
    if filelist == os.listdir("../Data/TenExSpectra_JSON"):
        for i in range(len(filelist)):
            filelist[i] = "../Data/TenExSpectra_JSON/"+filelist[i]
    
    for filepath in filelist:
        dict = ReadJson(filepath)
        X = dict["SpectralX"]
        for key in dict:
            if key != "SpectralX":
                #dftemp = pd.DataFrame({"Excitation": dict[key]["Excitation"], "Xdata": X, "Reflectivity": dict[key]["Data"],\
                #                        "Baseline": dict[key]["baseline"], "Peak": dict[key]["peak"], "FHHM points": dict[key]["FWHM"]},dtype = object)
                dftemp.at[1,"Excitation"] = dict[key]["Excitation"]
                dftemp.at[1,"Baseline"] = dict[key]["baseline"]
                dftemp.at[1,"Peak"] = dict[key]["peak"]
                dftemp.at[1,"FWHM points"] = dict[key]["FWHM"]
                for i in range(len(X)):
                    dftemp.at[1,str(X[i])] = dict[key]["Data"][i]
                dataf = pd.concat([dataf, dftemp], ignore_index = True)
    print("Dataframe loaded")
    
    return dataf