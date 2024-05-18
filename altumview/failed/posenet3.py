
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
# from scratch import *

no_joints=18
no_coord=2
window_size = 30

posex = []
posey = []
skel_data = []

def extrapolate_data(data, expected_length, default_value):
    if len(data) < expected_length:
        data += [default_value] * (expected_length - len(data))
    return data

def pose_net(json_file_path):

    with open(json_file_path, 'r') as data_file:
        data = json.load(data_file)

    expected_length = 5  
    default_value = 0    
    
    posex = data['Posex']
    posey = data['Posey']
    no_joints = 18
    no_coord = 2
    window_size = 30
    
    # number of frames to nearest number
    total_elements = int((len(posex) // (no_joints * no_coord)) * no_joints * no_coord)

    # cut the posex and posey to the nearest number of frames
    truncated_posex = posex[:total_elements]
    truncated_posey = posey[:total_elements]
    reshaped_posex = np.reshape(truncated_posex, (-1, no_joints))
    reshaped_posey = np.reshape(truncated_posey, (-1, no_joints))
    
    # form skel_data with shape (2, num_frames, no_joints)
    skel_data = np.array([reshaped_posex, reshaped_posey])
    skel_data = np.transpose(skel_data, (1, 2, 0))

    segment = skel_data[0:window_size, :, :]
    print(f"Shape of segment being passed to skel_comp: {segment.shape}")

    # skel_comp to get the recon_sig_x and recon_sig_y
    encoding_x, encoding_y, recon_sig, recon_sig_x, recon_sig_y = skel_comp(segment, window_size, no_joints, no_coord, device='openpose')
    encoding_x = extrapolate_data(encoding_x, expected_length, default_value)
    encoding_y = extrapolate_data(encoding_y, expected_length, default_value)
    print(f"Encoding X: {encoding_x}")
    print(f"Encoding Y: {encoding_y}")

    return recon_sig_x, recon_sig_y

pose_net('/Users/Downloads/combined_coordinates (2).json')
