import os
import json
import tkinter as tk
import pandas as pd
from openpyxl import load_workbook
from tkinter import filedialog


def ChooseFiles(initdir = ".."):
    # Initialise tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Prompt to choose the files to process.
    files = filedialog.askopenfilenames(initialdir = initdir)
    
    # Return filenames as simple list
    return files

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

def xlsxToDict(filepath):
    # Read xlsx file, rewrite to a dictionary for JSON. Only choose sheet with correct data.
    PandasFrame = pd.read_excel(filepath,sheet_name = None)
    sheet = PandasFrame["Sheet1 (2)"]
    
    # dict will be the output dictionary, matrixform simply an array form of the Panda Dataframe
    dict = {}
    matrixform = []
    for column in sheet:
        col = [column]
        for elem in sheet[column]:
            col.append(elem)
        matrixform.append(col)
    
    # Dictionary will be arranged according to excitations
    dict["SpectralX"] = matrixform[0][6:]
    for column in matrixform:
        if str(column[3]) != "nan" and str(column[6]) != "nan" and str(column[100]) != "nan":
            if str(column[4]) == "nan":
                dict["SpectralX"] = matrixform[0][6:]
                dict[str(int(column[3]))+" nm"] = {"Data": column[6:],    \
                                            "Excitation": column[3]         \
                                        }
            else:
                dict["SpectralX"] = matrixform[0][4:]
                dict[str(int(column[3]))+" nm"] = {"Data": list(column[4:]),    \
                                            "Excitation": column[3]         \
                                        }
    
    return dict



def main():
    files = ChooseFiles()
    print("Processing, please wait...")
    for file in files:
        dict = xlsxToDict(file)
        filename = file[file.rfind("/")+1:file.rfind(".")]
        WriteJson("../TenExSpectra_JSON/"+filename+".json",dict)
        print(filename+".json done")
    print("All done.")

if __name__ == "__main__":
    main()
