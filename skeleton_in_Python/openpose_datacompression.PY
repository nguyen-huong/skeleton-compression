#input: action, json data provided in openpose folder
#output: compressed data

from multiprocessing import Process
import numpy as np
import scipy.io
import array
import os
import json
from skel_compression import *

# set the path to the folder where the json files are
sourcepath="./open_pose/" #openpose datapath
path, folder1, files = next(os.walk(sourcepath))
elapsed=[]
# define the number of joints and coordinates
no_joints=18
no_coord=2
window_size = 30

#loop through all the files in the folder
for i in range(0,22):
    folder2_path=sourcepath+folder1[i]+'/'
    path, folder2, files = next(os.walk(folder2_path))
    posex=[]
    posey=[]
    skel_data=[]
    no_frames=len(files)

#loop through all the frames in each file, read the json file and store the data in a list
    for j in range(0,len(files)):
        filepath=folder2_path+files[j]
        with open(filepath) as data_file:
            data = json.load(data_file)
            posex.append(data['people'][0]['pose_keypoints'][0::3])  #x
            posey.append(data['people'][0]['pose_keypoints'][1::3])   #y

#convert the list to numpy array
    posex = np.array(posex)
    posey = np.array(posey)
    skel_data.append(posex)
    skel_data.append(posey)

#reshape the data to get the required format
    skel_data=np.array(skel_data)
    skel_data=np.reshape(skel_data, (no_frames,no_joints,no_coord))
    print(skel_data.shape)

#call the function to compress the data
    skel_comp(skel_data, no_frames, no_joints, no_coord, device='openpose')

