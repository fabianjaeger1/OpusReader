from brukeropusreader import read_file

import argparse
import sys

opus_data = read_file("LN-3083h_20200701_A.0")

print(f'Parsed fields: '
              f'{list(opus_data.keys())}')

print("test")
category = "Instrument"

print(f'Instrument: 'f'{opus_data[category]}')
#opus_data_instrument is of file type string
opus_data_instrument = (f'{opus_data[category]}')

#string = 


#print(f'Absorption spectrum: ' f'{opus_data["AB"]}')
print(type(opus_data_instrument))
#print(opus_data_instrument[3:15))
# opus_temperature = f'{opus_data_instrument["TSC"]}'

