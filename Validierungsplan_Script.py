'''
Make sure to run Python3 not Python2 (will yield an error with the f function)
'''

from numpy.lib.npyio import save
from brukeropusreader import read_file
import os
import argparse
import sys
import csv
import shutil
from collections import Counter
import pandas as pd 
import collections
import string
import matplotlib
import glob
import matplotlib.pyplot as plt
matplotlib.pyplot.switch_backend('agg')
import numpy as np
import seaborn as sns
import os

home_path = os.getcwd() #Path where the script is located
print(home_path)
figures_path = "%s/Validierungsplan_LaTeX/Figures" % home_path

my_cmap = sns.light_palette("Navy", as_cmap = True)
sns.set()

# Prompt variable input date

def createLaTeXDirectory(path_name):
    # path = ("%s/%s" % (home_path, path_name))
    path = "{}/{}".format(home_path, path_name)
    print(path)
    
    try:
         os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Succesfully created the directory %s" % path)

def createFiguresDirectory(path_name):
    #currentworkingdir = os.getcwd()
    #path = ("%s/%s/Figures" % (currentworkingdir,path_name))
    path = "{}/{}/Figures".format(home_path, path_name)
    
    try:
         os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Succesfully created the directory %s" % path)

date_release = input("Datum des Documentes (Titel): ")


def createLaTeXFileBericht():
    pathtemplate = "%s/Validierungsbericht_LaTeX_Template.tex" % home_path
    if os.path.exists(pathtemplate):
        createLaTeXDirectory("Validierungsbericht_LaTeX")
        createFiguresDirectory("Validierungsbericht_LaTeX")
        os.replace(pathtemplate, "{}/Validierungsbericht_LaTeX/ValidierungsberichtPHYDENT{}.tex".format(home_path,date_release))
        # newpath = "%s/Validierungsplan_LaTeX" % os.getcwd()
        # os.chdir(newpath)
        # filename = "ValidierungsplanPHYDENT%s.tex" % date_release
    else:
        path = "%s/Validierungsbericht_LaTeX" % home_path
        if os.path.exists(path):
            fileExt = r".tex"
            file = [_ for _ in os.listdir(path) if _.endswith(fileExt)]
            texfile = file[0]
            os.chdir(path)
            os.rename(texfile,"ValidierungsberichtPHYDENT%s.tex" % date_release)
        pass

def createLaTeXFilePlan():
    # currentworkingdir = os.getcwd()
    pathtemplate = "%s/Validierungsplan_LaTeX_Template.tex" % home_path
    if os.path.exists(pathtemplate):
        createLaTeXDirectory("Validierungsplan_LaTeX")
        createFiguresDirectory("Validierungsplan_LaTeX")
        os.replace(pathtemplate, "{}/Validierungsplan_LaTeX/ValidierungsplanPHYDENT{}.tex".format(home_path,date_release))
        # newpath = "%s/Validierungsplan_LaTeX" % os.getcwd()
        # os.chdir(newpath)
        # filename = "ValidierungsplanPHYDENT%s.tex" % date_release
    else:
        path = "%s/Validierungsplan_LaTeX" % home_path
        if os.path.exists(path):
            fileExt = r".tex"
            file = [_ for _ in os.listdir(path) if _.endswith(fileExt)]
            texfile = file[0]
            os.chdir(path)
            os.rename(texfile,"ValidierungsplanPHYDENT%s.tex" % date_release)
        pass
    # print(filename)
    #print(os.getcwd())
    # subprocess.check_call(['pdflatex', filename])
    # os.system("pdflatex ValidierungsplanPHYDENT%s.tex" % date_release)
    #print(currentworkingdir)
    #path = ("%s/Validierungsplan_LaTeX" % currentworkingdir)
    #os.chdir(path)
    #print(os.getcwd())
    #texfile = open("ValidierungsplanPHYDENT%s.tex" % date_release, "x")
    # texfile.close()
    
    #os.system("pdflatex %d/ValidierungsplanPHYDENT%s.tex" % (currentworkingdir, date_release))

#createLaTeXDirectory()

def copyTemplateGraphics():
    # home_path
    # figures_directory
    filenames = ['flussdiagram.png', 'flussdiagram2.png', 'phytax_logo.jpg', 'sampling_design.png']
    figures_path = "%s/Validierungsplan_LaTeX/Figures" % home_path
    valpath = "%s/Validierungsbericht_LaTeX" % home_path
    os.chdir(home_path)
    # print(os.getcwd())
    if os.path.isfile(filenames[0]):
        for i in filenames:
            print(i)
            os.rename("%s/%s" % (home_path, i), "%s/%s" % (figures_path, i))
            if os.path.exists(valpath):
                shutil.copyfile("{}/Validierungsplan_LaTeX/Figures/{}".format(home_path,i), "{}/Validierungsbericht_LaTeX/Figures/{}".format(home_path,i))
            #os.rename()

createLaTeXFilePlan()
createLaTeXFileBericht()
copyTemplateGraphics()

def save_var_latex(key,value,path_name):
        # data_path = "%s/" % home_path
        data_path = "{}/{}".format(home_path, path_name)
        os.chdir(data_path)
        dict_var = {}
        file_path = os.path.join(os.getcwd(), "pythonvariables.dat")

        try:
            with open(file_path, newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    dict_var[row[0]] = row[1]
        except FileNotFoundError:
            pass

        dict_var[key] = value

        with open(file_path, "w") as f:
            for key in dict_var.keys():
                f.write(f"{key},{dict_var[key]}\n")

def inputinfo():
    versEuPh =input("Version Europ??ische Pharmakop??e: ")
    nrproducts = input("Anzahl an Produkten: ")
    nrgranulatcharges = input("Anzahl an Granulatchargen: ")

    dir = ["Validierungsplan_LaTeX", "Validierungsbericht_LaTeX"]
    for i in dir:
        save_var_latex('versEuPH', versEuPh, i)
        save_var_latex('nrProducts', nrproducts, i)
        save_var_latex('nrGranulatcharges', nrgranulatcharges,i)
        save_var_latex('dateRelease', date_release, i)

# Transfer Variables from Python to a .dat file once into Validierungsbericht and once in Validierungsplan
inputinfo()
opus_files = []


def Pruefdatenfiles():
    #Path where figures will be saved
    #print(os.getcwd())
    #os.chdir("../..")
    #print(os.getcwd())
    #home_path = "/home/fjaeg/Developer/OpusReader" 
    # def printfiles():
    #     path = "/home/fjaeg/Developer/OpusReader/Pruefdaten"
    #     #print(os.getcwd())
    #     os.chdir(path)
    #     filetypes = [".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9"]
    #     for file in os.listdir():
    #         if file.endswith(tuple(filetypes)):
    #             opus_files.append(file)
    # printfiles()

    def printfiles():
        #path = "/home/fjaeg/Developer/OpusReader/Pruefdaten"
        # workingdirectory = os.getcwd()
        os.chdir("%s/Pruefdaten" % home_path)
        path = os.getcwd()
        filetypes = [".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9"]
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(tuple(filetypes)):
                    opus_files.append(os.path.join(root,file))
    printfiles()
    #print(opus_files)
Pruefdatenfiles()

temperatures = []
temperatures_rf = []
serial_numbers = []
relhum = []
relhum_rf = []
abshum= []
abshum_rf = []
operators = []

offset = 6

def retrieve_temperature(opus_data, opus_data_rf):
    if ('TSC' in opus_data) and ('MVD' in opus_data):
        index1 = opus_data.find('TSC')
        index2 = opus_data.find(", 'MVD'")
        temperature = opus_data[(index1+offset): (index2)] 
    else:
        temperature = np.nan
    if ('TSC' in opus_data_rf) and ('MVD' in opus_data_rf):
        index1_rf = opus_data_rf.find('TSC')
        index2_rf = opus_data_rf.find(", 'MVD'")
        temperature_rf = opus_data_rf[(index1_rf+offset): (index2_rf)]
    else:
        temperature_rf = np.nan
    return [temperature, temperature_rf]

def retrieve_serialnumber(opus_data):
    index1 = opus_data.find('SRN')
    index2 = opus_data.find(", 'PKA'")

    serial_number = opus_data[(index1+offset+1): (index2-1)]
    return serial_number

def retrieve_operator(opus_data):
    index1 = opus_data.find('CNM')
    index2 = opus_data.find(", 'CPY'")
    operator = opus_data[(index1+offset+1): (index2-1)]
    return operator

def retrieve_abshum(opus_data, opus_data_rf):
    if ('HUA' in opus_data) and ('VSN' in opus_data):
        index1 = opus_data.find('HUA')
        index2 = opus_data.find(", 'VSN'")
        abshum = opus_data[(index1+offset): (index2)]
    else:
        abshum = np.nan
    if ('HUA' in opus_data_rf) and ('VSN' in opus_data_rf):    
        index1_rf = opus_data_rf.find('HUA')
        index2_rf = opus_data_rf.find(", 'VSN'")
        abshum_rf = opus_data_rf[(index1_rf + offset): (index2_rf)]
    else:
        absum_rf = np.nan
    return [abshum, abshum_rf]

def retrieve_relhum(opus_data, opus_data_rf):
    if ('HUM' in opus_data) and ('RSN' in opus_data):
        index1 = opus_data.find('HUM')
        index2 = opus_data.find(", 'RSN'")
        relhum = opus_data[(index1+offset): (index2)]
    else:
        relhum = np.nan
    if ('HUM' in opus_data_rf) and ('RSN' in opus_data_rf):
        index1_rf = opus_data_rf.find('HUM')
        index2_rf = opus_data_rf.find(", 'RSN'")
        relhum_rf = opus_data_rf[(index1_rf + offset): (index2_rf)]
    else:
        relhum_rf = np.nan
    return [relhum, relhum_rf]
    
#print(opus_files)

def opusinfo():
    for i in opus_files:
        opus_data = read_file(i)
        opus_data_instrument = (f'{opus_data["Instrument"]}')
        opus_data_instrument_rf = (f'{opus_data["Instrument (Rf)"]}')
        opus_data_sample = (f'{opus_data["Sample"]}')
        
        temperature_array = retrieve_temperature(opus_data_instrument, opus_data_instrument_rf)
        relhum_array = retrieve_relhum(opus_data_instrument, opus_data_instrument_rf)
        abshum_array = retrieve_abshum(opus_data_instrument, opus_data_instrument_rf)

        temperatures.append(temperature_array[0])
        temperatures_rf.append(temperature_array[1])
        serial_numbers.append(retrieve_serialnumber(opus_data_instrument))
        relhum.append(relhum_array[0])
        relhum_rf.append(relhum_array[1])
        abshum.append(abshum_array[0])
        abshum_rf.append(abshum_array[1])
        operators.append(retrieve_operator(opus_data_sample))

#opusinfo()# print(f'{opus_data["Instrument"]}')     
#print(relhum)
#print(abshum)
#print(operators)
opusinfo()

def createplots():
    # print(os.getcwd())
    os.chdir("../Validierungsplan_LaTeX/Figures")
    # print(os.getcwd())

    def analyst_plot(operator):
        dictoperator = collections.Counter(operator)
        dictoperator = dict(dictoperator)

        sorted_dictoperator_tuples = sorted(dictoperator.items(), key=lambda item: item[1], reverse=True)
        dictoperator_sorted = {k: v for k, v in sorted_dictoperator_tuples}
        # print(dictoperator_sorted)
        alphabet_string = string.ascii_lowercase
        alphabet_list = list(alphabet_string)
        for i,k in dictoperator_sorted.items():
            dictoperator_sorted = dict(zip(alphabet_list, list(dictoperator_sorted.values())))
        fig, ax = plt.subplots(1,1,figsize = (7, 7)) 
        ax.bar(dictoperator_sorted.keys(), dictoperator_sorted.values())
        ax.set_title(r"Anzahl gemessene Spektren pro Analyst")
        ax.set_ylabel(r"Anzahl Spektren")
        plt.savefig("analyst_plot.pdf")
        plt.show()


    def relhum_plot(relhum, relhum_rf):
        #os.chdir(home_path)
        fig, ax = plt.subplots(1,1,figsize = (7, 7)) 
        relhum = np.array(relhum).astype(np.float) 
        relhum = relhum[np.logical_not(np.isnan(relhum))]
        relhum_rf = np.array(relhum_rf).astype(np.float)
        relhum = relhum_rf[np.logical_not(np.isnan(relhum_rf))]
        data = [relhum, relhum_rf]
        def box_plot(data, edge_color, fill_color):
            bp = ax.boxplot(data, patch_artist=True)
            plt.setp(bp['medians'] ,color='tomato')
            for element in ['boxes', 'whiskers', 'fliers', 'means', 'caps']:
                plt.setp(bp[element], color=edge_color)

            for patch in bp['boxes']:
                patch.set(facecolor=fill_color)

        box_plot(data,'gray','lightgray')
        ax.set_title(r"Relative Luftfeuchtigkeit im Ger??t")
        ax.set_ylabel(r"Rel. Luftfeuchtigkeit $[\%]$")
        ax.set_xticklabels(['Probenmessung', 'Hintergrundmessung'])
        plt.tight_layout()
        plt.savefig('rehum_plot.pdf')
        plt.show()

    def abshum_plot(abshum, abshum_rf):
        #os.chdir(home_path)
        fig, ax = plt.subplots(1,1,figsize = (7, 7)) 
        abshum = np.array(abshum).astype(np.float) 
        abshum = abshum[np.logical_not(np.isnan(abshum))]
        abshum_rf = np.array(abshum_rf).astype(np.float)
        abshum_rf = abshum_rf[np.logical_not(np.isnan(abshum_rf))]
        data = [abshum, abshum_rf]
        def box_plot(data, edge_color, fill_color):
            bp = ax.boxplot(data, patch_artist=True)
            plt.setp(bp['medians'] ,color='tomato')
            for element in ['boxes', 'whiskers', 'fliers', 'means', 'caps']:
                plt.setp(bp[element], color=edge_color)

            for patch in bp['boxes']:
                patch.set(facecolor=fill_color)

        box_plot(data,'gray','lightgray')
        ax.set_title(r"Absolute Luftfeuchtigkeit im Ger??t")
        ax.set_ylabel(r"Luftfeuchtigkeit $[g/m^3]$")
        ax.set_xticklabels(['Probenmessung', 'Hintergrundmessung'])
        plt.tight_layout()
        plt.savefig('abshum_plot.pdf')
        plt.show()

    def temperature_plot(temp, temp_rf):
        #os.chdir(home_path)
        fig, ax = plt.subplots(1,1,figsize = (7, 7)) 
        temp = np.array(temp).astype(np.float) 
        temp = temp[np.logical_not(np.isnan(temp))]
        temp_rf = np.array(temp_rf).astype(np.float)
        temp_rf = temp_rf[np.logical_not(np.isnan(temp_rf))]
        data = [temp, temp_rf]
        def box_plot(data, edge_color, fill_color):
            bp = ax.boxplot(data, patch_artist=True)
            plt.setp(bp['medians'] ,color='tomato')
            for element in ['boxes', 'whiskers', 'fliers', 'means', 'caps']:
                plt.setp(bp[element], color=edge_color)

            for patch in bp['boxes']:
                patch.set(facecolor=fill_color)

        box_plot(data,'gray','lightgray')
        ax.set_title(r"Temperatur am Sensor")
        ax.set_ylabel(r"Temperatur [C$^{\circ}]$")
        ax.set_xticklabels(['Probenmessung', 'Hintergrundmessung'])
        plt.tight_layout()
        plt.savefig('temp_plot.pdf')
        plt.show()
    
    def numberdevices_plot(serial):
        nrDeviceA = serial.count('1 01938')
        nrDeviceB = serial.count('1 05305')
        nrDevices = [nrDeviceA, nrDeviceB]
        fig, ax = plt.subplots(1,1,figsize = (10,7))
        langs = ["A", "B"]
        ax.bar(langs, nrDevices)
        ax.set_ylabel("Anzahl Spektren")
        ax.set_title("Anzahl gemessene Spektren pro Ger??t")
        plt.tight_layout()
        plt.savefig('nr_measurementsdevices.pdf')
        plt.show()
    temperature_plot(temperatures, temperatures_rf)
    analyst_plot(operators) #works
    numberdevices_plot(serial_numbers) #works
    abshum_plot(abshum, abshum_rf)
    relhum_plot(relhum,relhum_rf)
createplots()

def compileLatex():
    path = "%s/Validierungsplan_LaTeX" % home_path
    os.chdir(path)
    file_name = "ValidierungsplanPHYDENT%s" %date_release
    os.system("pdflatex %s" % file_name)
    os.system("pdflatex %s" % file_name)
    # Has to be compiled twice due to LaTeX references

compileLatex()



# def categories():
#     os.chdir(home_path)
#     opus_data = read_file("LN-3083i_20200702_B.0")
#     print(f'Parsed fields: 'f'{list(opus_data.keys())}')
#     opus_data_instrument = (f'{opus_data["AB Data Parameter"]}')
#     print(opus_data_instrument)

# categories()