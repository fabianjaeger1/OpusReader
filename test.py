from brukeropusreader import read_file

import argparse
import sys

opus_data = read_file("LN-3083h_20200701_A.0")
opus_data2 = read_file("LN-3083i_20200702_B.0")

print(f'Parsed fields: '
              f'{list(opus_data.keys())}')

#Instrument Information
opus_data_instrument = (f'{opus_data["Instrument"]}')
opus_data_instrument_rf = (f'{opus_data["Instrument (Rf)"]}')
opus_data2_instrument = (f'{opus_data["Instrument"]}')
opus_data2_instrument_rf = (f'{opus_data["Instrument"]}')

index1 = opus_data2_instrument.find('TSC')
index2 = opus_data2_instrument.find(", 'MVD'")
offset= 6
temperature =opus_data2_instrument[(index1+offset): (index2)]
print(opus_data2_instrument)
print(temperature)

# Temperature

def retrieve_Temperature():
    index1 = opus_data_instrument.find('TSC')
    index2 = opus_data_instrument.find(", 'MVD'")
    index1_rf = opus_data_instrument_rf.find('TSC')
    index2_rf = opus_data_instrument_rf.find(", 'MVD'")
    offset = 6

    temperature = opus_data_instrument[(index1+offset): (index2)]   
    temperature_rf = opus_data_instrument_rf[(index1_rf+offset): (index2_rf)]
    return [temperature, temperature_rf]

#Parse Serial Number
def serialnumber():
    index1 = opus_data_instrument.find('SRN')
    index2 = opus_data_instrument.find(", 'PKA'")
    index1_rf = opus_data_instrument_rf.find('SRN')
    index2_rf = opus_data_instrument_rf.find(", 'PKA'")
    offset = 6
    serial_number = opus_data_instrument[(index1+offset+1): (index2-1)]
    serial_number_rf = opus_data_instrument_rf[(index1_rf+offset+1): (index2_rf-1)]
    return [serial_number, serial_number_rf]

print(serialnumber())
#print(opus_data_instrument)
#print(opus_data_instrument_rf)


#print(opus_data_instrument)
#opus_data_instrument is of file type string

#string = 


#print(f'Absorption spectrum: ' f'{opus_data["AB"]}')
print(type(opus_data_instrument))
#print(opus_data_instrument[3:15))
# opus_temperature = f'{opus_data_instrument["TSC"]}'

