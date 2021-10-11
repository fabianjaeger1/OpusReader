from brukeropusreader import read_file

import os
import argparse
import sys
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
matplotlib.pyplot.switch_backend('agg')
import numpy as np
import seaborn as sns
#st = sns.axes_style("ticks")
#sns.set(style = st,palette=sns.color_palette("muted"), rc={'figure.figsize': (12,12)})
#print(os.listdir())

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern Roman"]})
my_cmap = sns.light_palette("Navy", as_cmap = True)
sns.set()
home_path = "/home/fjaeg/Developer/OpusReader"

opus_files = []
def printfiles():
    path = "/home/fjaeg/Developer/OpusReader/Achyranthis bidentatae radix"
    print(os.getcwd())
    os.chdir(path)
    filetypes = [".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9"]
    for file in os.listdir():
        if file.endswith(tuple(filetypes)):
            opus_files.append(file)
printfiles()

temperatures = []
temperatures_rf = []
serial_numbers = []
serial_numbers_rf = []

def retrieve_temperature(opus_data, opus_data_rf):
    index1 = opus_data.find('TSC')
    index2 = opus_data.find(", 'MVD'")
    index1_rf = opus_data_rf.find('TSC')
    index2_rf = opus_data_rf.find(", 'MVD'")
    offset = 6
    temperature = opus_data[(index1+offset): (index2)]   
    temperature_rf = opus_data_rf[(index1_rf+offset): (index2_rf)]
    return [temperature, temperature_rf]

def retrieve_serialnumber(opus_data, opus_data_rf):
    index1 = opus_data.find('SRN')
    index2 = opus_data.find(", 'PKA'")
    index1_rf = opus_data_rf.find('SRN')
    index2_rf = opus_data_rf.find(", 'PKA'")
    offset = 6
    serial_number = opus_data[(index1+offset+1): (index2-1)]
    serial_number_rf = opus_data_rf[(index1_rf+offset+1): (index2_rf-1)]
    return [serial_number, serial_number_rf]

 
print(opus_files)
def opusinfo():
    for i in opus_files:
        opus_data = read_file(i)
        opus_data_instrument = (f'{opus_data["Instrument"]}')
        opus_data_instrument_rf = (f'{opus_data["Instrument (Rf)"]}')
        
        temperature_array = retrieve_temperature(opus_data_instrument, opus_data_instrument_rf)
        serial_array = retrieve_serialnumber(opus_data_instrument, opus_data_instrument_rf)

        temperatures.append(temperature_array[0])
        temperatures_rf.append(temperature_array[1])
        serial_numbers.append(serial_array[0])
        serial_numbers_rf.append(serial_array[1])
                

opusinfo()# print(f'{opus_data["Instrument"]}')     
print(temperatures)
print(temperatures_rf)
print(serial_numbers)
print(serial_numbers_rf)

def temperature_plot(temp, temp_rf):
    os.chdir(home_path)
    fig, ax = plt.subplots(1,1,figsize = (10, 7)) 
    temp = np.array(temp).astype(np.float) 
    temp_rf = np.array(temp_rf).astype(np.float)
    data = [temp, temp_rf]
    def box_plot(data, edge_color, fill_color):
        bp = ax.boxplot(data, patch_artist=True)
        plt.setp(bp['medians'],color='red')
        for element in ['boxes', 'whiskers', 'fliers', 'means', 'caps']:
            plt.setp(bp[element], color=edge_color)

        for patch in bp['boxes']:
            patch.set(facecolor=fill_color)

    box_plot(data,'black','lightblue')
   # bplot1 = plt.boxplot(data, patch_artist=True)
    ax.set_title("Temperatur am Sensor")
    ax.set_ylabel("Temperatur")
    ax.set_xticklabels(['Probenmessung', 'Hintergrundmessung'])
    plt.savefig('temp_plot.pdf')
    plt.show()
 
def numberdevices_plot(serial, serial_rf):
    nrDeviceA = serial.count('1 01938')
    nrDeviceB = serial.count('1 05305')
    data = [nrDeviceA, nrDeviceB]
    fig, ax = plt.subplots(1,1,figsize = (10,7))
    langs = ["A", "B"]
    ax.bar(langs, data)
    ax.set_ylabel("Anzahl Spektren")
    ax.set_title("Anzahl gemessene Spektren pro Geraet")
    plt.savefig('nr_measurementsdevices.pdf')
    plt.show()

temperature_plot(temperatures, temperatures_rf)
numberdevices_plot(serial_numbers, serial_numbers_rf)



# def opusdata():
#   opus_data = read_file("LN-3083h_20200701_A.0")
#   opus_data2 = read_file("LN-3083i_20200702_B.0")
#
#   print(f'Parsed fields: '
#            f'{list(opus_data.keys())}')
#

#Instrument Information
#    opus_data_instrument = (f'{opus_data["Instrument"]}')
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
#print(opus_data_instrument)
#print(opus_data_instrument_rf)


#print(opus_data_instrument)
#opus_data_instrument is of file type string

#string = 


#print(f'Absorption spectrum: ' f'{opus_data["AB"]}')
#print(type(opus_data_instrument))
#printfiles()            
#print(opus_files)
#print(opus_data_instrument[3:15))
# opus_temperature = f'{opus_data_instrument["TSC"]}'

