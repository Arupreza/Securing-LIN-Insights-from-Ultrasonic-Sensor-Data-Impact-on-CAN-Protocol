#import libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Data_Prep import *


cols = ["No", "Time_Offset", "Type", "CAN_ID", "Data_Length"] + [f'Payload_{i}' for i in range(1, 9)]

#importing dataset
def Convert_to_df(path):
    if path[-3:] == "trc":
        data_df = Convert_from_trc(path)[17:]
    elif path[-3:] == "txt": 
        data_df = Convert_from_txt(path)
    else:
        print("Error, not suitable file")
        exit()
    return data_df


def Convert_from_trc(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split(" ")
        b.append(list(filter(('').__ne__, temp)))
    final = pd.DataFrame(b, columns = cols)
    return final


#importing dataset
def Convert_from_txt(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split("\t")
        b.append(list(filter(('').__ne__, temp)))
    final = pd.DataFrame(b, columns = cols)
    return final