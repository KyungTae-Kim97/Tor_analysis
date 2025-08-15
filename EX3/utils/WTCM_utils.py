import numpy as np
from math import floor, ceil
import dpkt
import csv
import socket
import os
import pandas as pd

def get_src_ip(pcap_file):
	pcap = dpkt.pcap.Reader(open(pcap_file, 'rb'))
	try:
		for timestamp, buf in pcap:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src_ip = socket.inet_ntoa(ip.src)
			
			return src_ip
	except AttributeError:
		pass
	except dpkt.dpkt.UnpackError:
		pass
	except dpkt.dpkt.NeedData:
		pass

def sign(x):
    return 1 if x > 0 else -1

def calculate_cluster(timestamps, window_length = 0.044):
    if not timestamps:
        return 0

    # Sort timestamps in case they are not ordered
    timestamps = sorted(timestamps)
    threshold = window_length / 10.0

    cluster_count = 1  # At least one cluster exists
    for i in range(1, len(timestamps)):
        if timestamps[i] - timestamps[i - 1] > threshold:
            cluster_count += 1

    return cluster_count

def calculate_WTCM(F, w=0.044, N=2000, C=3):
    # Initialize the WTCM matrix with zeros: shape (2C + 2, N)
    M = np.zeros((2 * C + 2, N), dtype=int)
    
    I_window = 1  # curr of timestamps in the current window
    T_window = []  # list
    
    for tk, lk in F:#ent window index
        dk = sign(lk)
        ck = min(int(abs(lk) / 512), C)

        j = min(floor(tk / w) + 1, N)
        i = 2 * ck + (0 if dk > 0 else 1)
        # Update the WTCM count
        M[i, j - 1] += 1  # convert to 0-based indexing

        if j != I_window:
            M[2 * C, j - 1] = j - I_window  # row 2C + 1 (index 2C)
            cluster_v = calculate_cluster(T_window)  # row 2C + 2 (index 2C + 1)
            M[2 * C + 1, I_window - 1] = cluster_v  # row 2C + 2 (index 2C + 1)
            I_window = j
            T_window = [tk]
        else:
            T_window.append(tk)
    return M

def getAtr(pcap_path, src_ip, num_pkts_cut):

    fd = open(pcap_path, 'rb')
    pcap = dpkt.pcap.Reader(fd)

    times = list()
    sizes = list()

    try:
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue
            if ip.p != dpkt.ip.IP_PROTO_TCP:
                continue
            if socket.inet_ntoa(ip.src) in src_ip:
                times.append(ts)
                sizes.append(1 * len(buf))
            else:
                times.append(ts)
                sizes.append(-1 * len(buf))

    except AttributeError:
        pass
    except dpkt.dpkt.UnpackError:
        pass
    except dpkt.dpkt.NeedData:
        pass
    
    if num_pkts_cut > 0:
        del times[:num_pkts_cut]
        del sizes[:num_pkts_cut]

    fd.close()
    times_start_0=[t - times[0] for t in times] 
    # print(times_start_0)
    # print(sizes)
    combined = list(zip(times_start_0, sizes))
    return combined