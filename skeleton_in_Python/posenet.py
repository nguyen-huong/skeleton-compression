#input: posex, posey, window size, number of joints, number of coordinates
#output: compressed data

from multiprocessing import Process
import numpy as np
import scipy.io
import array
import os
import json
from skel_compression import *
from huffman import *
from timer_cm import Timer

# set the path to the folder where the json files are
no_joints=17
no_coord=2
window_size = 30

# create a folder to store the compressed data
posex = []
posey = []
skel_data = []

# function to compr
def pose_net(posedata, j):
    with open(posedata, 'r') as data_file:
        global posex
        global posey
        global skel_data
        posex = []
        posey = []
        skel_data = []
        no_joints = 17 # number of joints
        no_coord = 2 # number of coordinates
        window_size = 30 # window size
        data = json.load(data_file)
        posex.append(data['Posex'])  # x
        posey.append(data['Posey'])  # y
        posex = np.array(posex) # convert to numpy array
        posey = np.array(posey) # convert to numpy array

        # reshape the data
        skel_data.append(np.reshape(posex, (-1, 17)))
        skel_data.append(np.reshape(posey, (-1, 17)))
        skel_data = np.array(skel_data)

        #send skel_data to huffman coding to see how much compression making
        no_coord, no_frames, no_joints = skel_data.shape
        skel_data = np.reshape(skel_data, (no_frames, no_joints, no_coord))
        encoding_x, encoding_y, recon_sig, recon_sig_x, recon_sig_y= skel_comp(skel_data[j:j+window_size, :, :], window_size, no_joints, no_coord, device='posenet')
        return recon_sig_x, recon_sig_y

# function get length of json file
def get_length(x):
    length = 0
    with open(x, 'r') as data_file:
        data = json.load(data_file)
        length = len(data['Posex'])
    return length

# function get number of frames
def get_frames(x):
    frames = 0
    with open(x, 'r') as data_file:
        data = json.load(data_file)
        frames = len(data['Posex'][0])
    return frames

def real_time(dict):
    #input: json dict of x, y coordinates
    #output: compressed data
    skel_data = dict
    posex = data["Posex"]
    posey = data["Posey"]
    skel_data.append(np.reshape(posex, (-1, 17)))
    skel_data.append(np.reshape(posey, (-1, 17)))
    skel_data = np.array(skel_data)
    no_coord, no_frames, no_joints = skel_data.shape
    skel_data = np.reshape(skel_data, (no_frames, no_joints, no_coord))
    skel_comp(skel_data[0:window_size, :, :], window_size, no_joints, no_coord, device='posenet')

# get the number of bits in the compressed data
def get_bits_from_json(json_file):
    with open(json_file, 'r') as data_file:
        data = json.load(data_file)
        #convert to bits
        for i in range(0, len(data['Posex'])):
            #convert float to int
            data['Posex'][i] = int(
                data['Posex'][i] * 100)  # convert to int
            data['Posex'][i] = bin(
                data['Posex'][i])[2:].zfill(8)  # convert to binary and add 0s at the beginning

        for i in range(0, len(data['Posey'])):
            data['Posey'][i] = int(
                data['Posey'][i] * 100)  # convert to int
            data['Posey'][i] = bin(
                data['Posey'][i])[2:].zfill(8)  # convert to binary and add 0s at the beginning

        # get total length of the binary string
        x_total_length= 0
        for i in range(0, len(data['Posex'])):
            x_total_length += len(data['Posex'][i])
        y_total_length= 0
        for i in range(0, len(data['Posey'])):
            y_total_length += len(data['Posey'][i])
        print('Before compression X in bits:', x_total_length, 'Before compression Y in bits:', y_total_length)


# get frames from json file
def get_frames(x):
    frames = 0
    with open(x, 'r') as data_file:
        data = json.load(data_file)
        frames = len(data['Posex'])
    # print(frames)
    return int(frames)

# make sure the length of the json file is divisible by 30
length = get_frames(file)
ln = int(np.floor(length / 30))*30

# loop through the json file and compress each 30 frames
pose_xr = []
pose_yr = []
for i in range(0, ln, 30):
    try:
        x_recon, y_recon = pose_net(file, i)
        pose_xr.append(x_recon)
        pose_yr.append(y_recon)
    except IndexError:
        pass

# reshape the reconstructed data
n1,n2,n3= np.array(pose_xr).shape
pose_xr = np.reshape(pose_xr, (n1*n2, n3))
pose_yr = np.reshape(pose_yr, (n1*n2, n3))

# throw exception if the length of the reconstructed data is not the same as the original data
if len(pose_xr) != len(posey):
    raise Exception('Length of reconstructed data is not the same as the original data')

# throw exception if there is any nan in the reconstructed data
if np.isnan(pose_xr).any() or np.isnan(pose_yr).any():
    raise Exception('There is nan in the reconstructed data')

if __name__=='__main__':
    # argument to get the path of the json file
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='data.json', help='path to the json file')
    parser.add_argument('--store', type=str, default='./reconstructed_signal/compressed_data.json', help='path to the json file')
    args = parser.parse_args()
    # run the main function
    answer = pose_net(args.file, 0, args.store)