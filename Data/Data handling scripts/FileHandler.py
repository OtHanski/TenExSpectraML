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

def ReadToPandas(filelist):
# Reads Json file, returns as pandas dataframe with columns as listed below
    column_names = ["Excitation", "Baseline", "Peak", "FWHM points", "Xdata", "Reflectivity"]
    dataf = pd.DataFrame(columns = column_names, dtype = object)
    dataf
    dataf["Xdata"].astype(object)
    dataf["Reflectivity"].astype(object)
    dataf["FWHM points"].astype(object)
    dftemp = dataf
    
    for filepath in filelist:
        dict = ReadJson(filepath)
        X = dict["SpectralX"]
        for key in dict:
            if key != "SpectralX":
                #dftemp = pd.DataFrame({"Excitation": dict[key]["Excitation"], "Xdata": X, "Reflectivity": dict[key]["Data"],\
                #                        "Baseline": dict[key]["baseline"], "Peak": dict[key]["peak"], "FHHM points": dict[key]["FWHM"]},dtype = object)
                dftemp.at[1,"Excitation"] = dict[key]["Excitation"]
                print(dftemp)
                dftemp.at[1,"Xdata"] = X
                dftemp.at[1,"Reflectivity"] = dict[key]["Data"]
                dftemp.at[1,"Baseline"] = dict[key]["baseline"]
                dftemp.at[1,"Peak"] = dict[key]["peak"]
                dftemp.at[1,"FWHM points"] = dict[key]["FWHM"]
                dataf = pd.concat([dataf, dftemp], ignore_index = True)
    
    dataf.tail()
    return dataf
        
# Not used
def ReadTXT(filepath):
    # Reads a txt into a string
    f = open(filepath,"r")
    string = f.read()
    return string

# Not used
def ConvertDAT(settings,instr,arg):

    files = ChooseFiles(settings["FILE"]["ROOTFOLDER"])
    convfolder = files[0][:files[0].rfind("/")]+"/converted"
    CheckFolder(convfolder)
    
    for filename in files:
        convfile = convfolder+filename[filename.rfind("/"):-5]+".dat"
        data = ReadJson(filename)
        filetype = data["metadata"]["filetype"]
        
        time = data["time"]["data"]
        
        datakey = ["time"]
        writedata = [time]
        writestr = "#"
        
        if filetype == "measurement":
            for chan in data["Channels"]:
                Voltage = data["Channels"][chan]["Voltage"]
                if len(Voltage) != 0:
                    datakey.append(chan)
                    writedata.append(Voltage)
            for key in datakey:
                writestr += key+"\t"
            
        if filetype == "statistics":
            Integral = None
            IntError = None
            for chan in data["Channels"]:
                Voltage = data["Channels"][chan]["avg"]
                if len(Voltage) != 0:
                    datakey.append(chan)
                    writedata.append(Voltage)
                try:
                    Integral = data["Channels"][chan]["Integral"]
                    IntError = data["Channels"][chan]["Intdev"]
                except KeyError:
                    None
            for key in datakey:
                writestr += key+"\t"
            writestr += "\n# Integral: "+str(Integral)+"\n#Integral Error: "+str(IntError)
        
        for i in range(len(time)):
            writestr += "\n"
            for j in range(len(datakey)):
                writestr += str(writedata[j][i])+"\t"
        
        f = open(convfile, "w")
        f.write(writestr)
        f.close()