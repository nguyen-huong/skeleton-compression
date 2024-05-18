from multiprocessing import Process
import numpy as np
import scipy.io
import array
# import pandas as pd
import os
import json
from skel_compression_1 import *
from huffman import *
from timer_cm import Timer

no_joints = 18
no_coord = 2
window_size = 30

def load_and_process_coordinates(x_file_path, y_file_path, no_joints=18):
    # attempt to read x and y separately
    with open(x_file_path, 'r') as x_file:
        x_data_raw = x_file.readlines()
    with open(y_file_path, 'r') as y_file:
        y_data_raw = y_file.readlines()
    # list to floats
    x_data = [float(num) for line in x_data_raw for num in line.strip().split()]
    y_data = [float(num) for line in y_data_raw for num in line.strip().split()]
    
    # reshape
    num_frames_x = len(x_data) // (no_joints * no_coord)
    num_frames_y = len(y_data) // (no_joints * no_coord)
    num_frames = min(num_frames_x, num_frames_y)
    
    # reshape to array [number of frames, no_joints, no_coord, 2] for x and y
    posex = np.array(x_data[:num_frames * no_joints * no_coord]).reshape(num_frames, no_joints, no_coord)
    posey = np.array(y_data[:num_frames * no_joints * no_coord]).reshape(num_frames, no_joints, no_coord)
    skel_data = np.stack((posex, posey), axis=-1)

    try:
        posex = skel_data[:, :, :, 0]
        posey = skel_data[:, :, :, 1]

        # call skell comp
        encoding_x, encoding_y, recon_sig, recon_sig_x, recon_sig_y = skel_comp(posex, posey, window_size, no_joints, no_coord, device='openpose')
        
        print(f"encoding_x: {encoding_x[:10]}")  
        print(f"encoding_y: {encoding_y[:10]}")
        
    except Exception as e:
        print(f"Error: {e}")
        return

    return recon_sig_x, recon_sig_y


     

x_file_path = '/Users/x_coordinates.txt'
y_file_path = '/Users/y_coordinates.txt'
load_and_process_coordinates(x_file_path, y_file_path)