import os

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

home_path = "/home/fjaeg/Developer/OpusReader" 
def categories():
    os.chdir(home_path)
    opus_data = read_file("LN-3083i_20200702_B.0")
    print(f'Parsed fields: 'f'{list(opus_data.keys())}')
    opus_data_instrument = (f'{opus_data["AB Data Parameter"]}')
    print(opus_data_instrument)
    print(f'{opus_data["Instrument"]}')     
#print(opus_data_instrument_rf)

categories()