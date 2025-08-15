import numpy as np
from math import floor, ceil
import dpkt
import csv
import socket
import os
import pandas as pd
from WTCM_utils import * 

DATADIR = '../dataset/crawl250610/0'
save_folder = '../dataset_feature/250610'

for folder_path, subfolders, files in os.walk(DATADIR):
    subfolders.sort()  # Sort folders alphabetically (modifies in-place)
    files.sort()       # Sort files alphabetically
    for file in files:
        if not file.endswith('.pcap'):
            continue
        
        pcap_path = os.path.join(folder_path, file)
        src_ip = get_src_ip(pcap_path)
        
        path_split = pcap_path.split("/")
        c_index = -3
        class_name = '_'.join(path_split[c_index:-1])

        try:
            packet_flow = getAtr(pcap_path, src_ip, 0) # error with path from pcap # result: packet time(list) & ingoing, outgoing size(list)
            
            data = calculate_WTCM(packet_flow)
            df = pd.DataFrame(data)
            df.to_csv(f'{save_folder}/{class_name}.csv', index=False, header=False)  # index=False -> no index

            # print(pcap_path)
            
        except Exception as e:
            print(e)
