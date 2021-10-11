from brukeropusreader import read_file

import os
import argparse
import sys
from collections import Counter
import pandas as pd 
import collections
import matplotlib
import matplotlib.pyplot as plt
matplotlib.pyplot.switch_backend('agg')
import numpy as np
import seaborn as sns
#st = sns.axes_style("ticks")
#sns.set(style = st,palette=sns.color_palette("muted"), rc={'figure.figsize': (12,12)})
#print(os.listdir())

# plt.rcParams.update({
#     "text.usetex": True,
#     "font.family": "serif",
#     "font.sans-serif": ["Computer Modern Roman"]})
my_cmap = sns.light_palette("Navy", as_cmap = True)
sns.set()

#Path where figures will be saved
home_path = "/home/fjaeg/Developer/OpusReader" 
opus_files = []
# def printfiles():
#     path = "/home/fjaeg/Developer/OpusReader/Pruefdaten"
#     #print(os.getcwd())
#     os.chdir(path)
#     filetypes = [".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9"]
#     for file in os.listdir():
#         if file.endswith(tuple(filetypes)):
#             opus_files.append(file)
# printfiles()

def printfiles2():
    path = "/home/fjaeg/Developer/OpusReader/Pruefdaten"
    #print(os.getcwd())
    os.chdir(path)
    filetypes = [".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9"]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(tuple(filetypes)):
                opus_files.append(os.path.join(root,file))
printfiles2()

temperatures = []
temperatures_rf = []
serial_numbers = []
relhum = []
relhum_rf = []
abshum= []
abshum_rf = []
operators = []

def retrieve_temperature(opus_data, opus_data_rf):
    index1 = opus_data.find('TSC')
    index2 = opus_data.find(", 'MVD'")
    index1_rf = opus_data_rf.find('TSC')
    index2_rf = opus_data_rf.find(", 'MVD'")
    offset = 6
    temperature = opus_data[(index1+offset): (index2)]   
    temperature_rf = opus_data_rf[(index1_rf+offset): (index2_rf)]
    return [temperature, temperature_rf]

def retrieve_serialnumber(opus_data):
    index1 = opus_data.find('SRN')
    index2 = opus_data.find(", 'PKA'")
    offset = 6
    serial_number = opus_data[(index1+offset+1): (index2-1)]
    return serial_number

def retrieve_operator(opus_data):
    index1 = opus_data.find('CNM')
    index2 = opus_data.find(", 'CPY'")
    offset = 6
    operator = opus_data[(index1+offset+1): (index2-1)]
    return operator

def retrieve_abshum(opus_data, opus_data_rf):
    index1 = opus_data.find('HUA')
    index2 = opus_data.find(", 'VSN'")
    index1_rf = opus_data_rf.find('HUA')
    index2_rf = opus_data_rf.find(", 'VSN'")
    offset = 6
    abshum = opus_data[(index1+offset): (index2)]
    abshum_rf = opus_data_rf[(index1_rf + offset): (index2_rf)]
    return [abshum, abshum_rf]

def retrieve_relhum(opus_data, opus_data_rf):
    index1 = opus_data.find('HUM')
    index2 = opus_data.find(", 'RSN'")
    index1_rf = opus_data_rf.find('HUM')
    index2_rf = opus_data_rf.find(", 'RSN'")
    offset = 6
    relhum = opus_data[(index1+offset): (index2)]
    relhum_rf = opus_data_rf[(index1_rf + offset): (index2_rf)]
    return [relhum, relhum_rf]
    
print(opus_files)
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

opusinfo()# print(f'{opus_data["Instrument"]}')     
# print(temperatures)
# print(temperatures_rf)
# print(serial_numbers)
print(relhum)
print(abshum)
print(operators)

def analyst_plot(operator):
    dictoperator = collections.Counter(operator)
    fig, ax = plt.subplots(1,1,figsize = (7, 7)) 
    ax.bar(dictoperator.keys(), dictoperator.values())
    ax.set_title(r"Anzahl gemessene Spektren pro Analyst")
    ax.set_ylabel(r"Anzahl Spektren")
    plt.savefig("analyst_plot.pdf")
    plt.show()


def relhum_plot(relhum, relhum_rf):
    os.chdir(home_path)
    fig, ax = plt.subplots(1,1,figsize = (7, 7)) 
    relhum = np.array(relhum).astype(np.float) 
    relhum_rf = np.array(relhum_rf).astype(np.float)
    data = [relhum, relhum_rf]
    def box_plot(data, edge_color, fill_color):
        bp = ax.boxplot(data, patch_artist=True)
        plt.setp(bp['medians'] ,color='tomato')
        for element in ['boxes', 'whiskers', 'fliers', 'means', 'caps']:
            plt.setp(bp[element], color=edge_color)

        for patch in bp['boxes']:
            patch.set(facecolor=fill_color)

    box_plot(data,'gray','lightgray')
    ax.set_title(r"Relative Luftfeuchtigkeit im Gerät")
    ax.set_ylabel(r"Rel. Luftfeuchtigkeit $[\%]$")
    ax.set_xticklabels(['Probenmessung', 'Hintergrundmessung'])
    plt.tight_layout()
    plt.savefig('rehum_plot.pdf')
    plt.show()

def abshum_plot(abshum, abshum_rf):
    os.chdir(home_path)
    fig, ax = plt.subplots(1,1,figsize = (7, 7)) 
    abshum = np.array(abshum).astype(np.float) 
    abshum_rf = np.array(abshum_rf).astype(np.float)
    data = [abshum, abshum_rf]
    def box_plot(data, edge_color, fill_color):
        bp = ax.boxplot(data, patch_artist=True)
        plt.setp(bp['medians'] ,color='tomato')
        for element in ['boxes', 'whiskers', 'fliers', 'means', 'caps']:
            plt.setp(bp[element], color=edge_color)

        for patch in bp['boxes']:
            patch.set(facecolor=fill_color)

    box_plot(data,'gray','lightgray')
    ax.set_title(r"Absolute Luftfeuchtigkeit im Gerät")
    ax.set_ylabel(r"Luftfeuchtigkeit $[g/m^3]$")
    ax.set_xticklabels(['Probenmessung', 'Hintergrundmessung'])
    plt.tight_layout()
    plt.savefig('abshum_plot.pdf')
    plt.show()

def temperature_plot(temp, temp_rf):
    os.chdir(home_path)
    fig, ax = plt.subplots(1,1,figsize = (7, 7)) 
    temp = np.array(temp).astype(np.float) 
    temp_rf = np.array(temp_rf).astype(np.float)
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
    ax.set_title("Anzahl gemessene Spektren pro Gerät")
    plt.tight_layout()
    plt.savefig('nr_measurementsdevices.pdf')
    plt.show()


# temperature_plot(temperatures, temperatures_rf)
# numberdevices_plot(serial_numbers)
# analyst_plot(operators)
# abshum_plot(abshum, abshum_rf)
# relhum_plot(relhum, relhum_rf)


# def opusdata():

#   opus_data2 = read_file("LN-3083i_20200702_B.0")

#print(f'Parsed fields: 'f'{list(opus_data.keys())}')
# opus_data_instrument = (f'{opus_data["Sample"]}')

#print(opus_data_instrument)


#Instrument Information

#    opus_data_instrument_rf = (f'{opus_data["Instrument (Rf)"]}')
#    opus_data2_instrument = (f'{opus_data["Instrument"]}')
#    opus_data2_instrument_rf = (f'{opus_data["Instrument"]}')

#    index1 = opus_data2_instrument.find('TSC')
#    index2 = opus_data2_instrument.find(", 'MVD'")
#    offset= 6
#    temperature =opus_data2_instrument[(index1+offset): (index2)]
#    print(opus_data2_instrument)
#    print(temperature)

# Temperature

def categories():
    os.chdir(home_path)
    opus_data = read_file("LN-3083i_20200702_B.0")
    print(f'Parsed fields: 'f'{list(opus_data.keys())}')
    opus_data_instrument = (f'{opus_data["AB Data Parameter"]}')
    print(opus_data_instrument)
#print(opus_data_instrument_rf)

categories()
#print(opus_data_instrument)
#opus_data_instrument is of file type string

#string = 


#print(f'Absorption spectrum: ' f'{opus_data["AB"]}')
#print(type(opus_data_instrument))
#printfiles()            
#print(opus_files)
#print(opus_data_instrument[3:15))
# opus_temperature = f'{opus_data_instrument["TSC"]}'

