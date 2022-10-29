# takes input of gft basis, define quantization matrix, utilize the quantization matrix to quantize data, and then use the quantization matrix to reconstruct the data
# input: gft basis, quantization matrix, data
# output: reconstructed data


from multiprocessing import Process
import collections
from collections import OrderedDict
import numpy as np
import scipy.io
import json
from scipy.fftpack import idct, dct
from huffman import *
import matplotlib.pyplot as plt
from read_skeleton import *
from rle import *

# define default quantization matrix
def quantization_matrix(window_size,no_joints):
    qt=np.ones((window_size,no_joints))
    inc=10
    for i in range (window_size):
        inc += 50
        qt[i,:]=inc*qt[i,:]

    qt[0,0]=100
    return qt

# define custom quantization matrix
def custom_qt(inc, sub, window_size, no_joints):
    qt = np.ones((window_size, no_joints))
    inc = inc
    for i in range(window_size):
        inc += sub
        qt[i, :] = inc * qt[i, :]
    return qt

# load the gft basis and quantization matrix
def graphconstruction_openpose():
    source_path_skelbasis="./gft_basis/skel_basis_openpose.mat" #trying to load the gft basis
    mat = scipy.io.loadmat(source_path_skelbasis)
    return mat['v']

def graphconstruction_kinect():
    source_path_skelbasis="./gft_basis/skel_basis.mat" #trying to load the gsf basis
    mat = scipy.io.loadmat(source_path_skelbasis)
    return mat['v']

def graphconstruction_posenet():
    source_path_skelbasis = "./gft_basis/posenet_gftbasis.mat"
    mat = scipy.io.loadmat(source_path_skelbasis)
    return mat['v']

def skel_comp(data, no_frames, no_joints, no_coord, device):
    #importing the skeleton gft basis
    if device =='openpose':
        v = graphconstruction_openpose()
    elif device =='kinect':
        v  = graphconstruction_kinect()
    elif device =='posenet':
        v  = graphconstruction_posenet()
    window_size=no_frames

   #compute the motion vector
    motion_vector=[]
    gft_coeff=[]
    for i in range(0,no_frames):

        temp=data[i,:,:]
        # make sure temp is not empty
        if temp.size != 0:
            raise ValueError('temp is empty')
            # throw exception if temp is not 2D
        if temp.ndim != 2:
            raise Exception('temp is not 2D')
      gft_coeff_temp=np.matmul(np.transpose(v), temp) #compute the gft coeff for each time frame
        gft_coeff.append(gft_coeff_temp)
    gft_coeff=np.array(gft_coeff)
    gft_dct_coeff=gft_coeff
    #temporal dct
    for k in range (no_joints):
        for l in range(no_coord):
            x=gft_coeff[:,k,l]
            gft_dct_coeff[:,k,l]=dct(x, norm='ortho')
            #input this into huffman
    qt=quantization_matrix(window_size,no_joints)  #non uniform quantization matrix
    # quantization
    gft_dct_coeff_round=np.zeros((no_frames,no_joints,no_coord))
    for l in range(no_coord):
        gft_dct_coeff_round[:,:,l]=(np.round(np.divide(gft_dct_coeff[:,:,l],qt),2))
    Q = np.array(gft_dct_coeff_round)
    x1 = np.squeeze(np.array(Q[:, :, 0]))
    y1 = np.squeeze(np.array(Q[:, :, 1]))

# flattening the array after quantization
    Q_flat = np.reshape(Q,((no_frames)*no_joints*no_coord),'C')
    x_flat = np.reshape(x1,(no_frames*no_joints),'C')
    y_flat = np.reshape(y1,(no_frames*no_joints),'C')
    Q_list = Q_flat.tolist()
    x_list = x_flat.tolist()
    y_list = y_flat.tolist()

    # get the index of the last non-zero element in the list
    nonzero = np.max(np.nonzero(Q_flat))
    nonzero_x = np.max(np.nonzero(x_flat))
    nonzero_y = np.max(np.nonzero(y_flat))

    # append the position to the array
    x_list_end1 = x_list[0:nonzero_x+1]
    y_list_end1 = y_list[0:nonzero_y+1]

    encoding_x, tree_x = Huffman_Encoding(x_list_end1)
    encoding_y, tree_y = Huffman_Encoding(y_list_end1)

    # after Huffman encoding, run length encoding
    rleencode_x = encode(encoding_x)
    rledecode_x = decode(rleencode_x)
    rleencode_y = encode(encoding_y)
    rledecode_y = decode(rleencode_y)

    # transfer encoding
    decoded_op_x=Huffman_Decoding(encoding_x, tree_x)
    decoded_op_y=Huffman_Decoding(encoding_y, tree_y)

    #input the last non zero element in the list
    nonzero1 = len(decoded_op_x)
    nonzero2 = len(decoded_op_y)

    nonzero1 = round(nonzero1)
    nonzero2 = round(nonzero2)

    # transfer the list to array
    window_length = (window_size * no_joints)
    numzero_x = window_length  - nonzero1
    numzero_y = window_length  - nonzero2
    x_final = np.append(decoded_op_x, np.zeros(numzero_x))
    y_final = np.append(decoded_op_y, np.zeros(numzero_y))

    #reconstruction
    #processing x and y separately
    reshape_x = np.reshape(x_final, (no_frames, no_joints), 'C')
    reshape_y = np.reshape(y_final, (no_frames, no_joints), 'C')

    #zero parting the array
    join_array=np.zeros((no_frames,no_joints,no_coord))
    join_array[:,:,0]=reshape_x
    join_array[:,:,1]=reshape_y

    #inverse quantization
    recon_sig_idct=np.zeros((no_frames,no_joints,no_coord))
    for l in range(no_coord):
        recon_sig_idct[:,:,l] = np.multiply(join_array[:,:,l],qt)

    #inverse dct
    recon_sig_idct=np.array(recon_sig_idct)
    for k in range (no_joints):
        for l in range(no_coord):
            y=recon_sig_idct[:,k,l]
            recon_sig_idct[:,k,l]=idct(y, norm='ortho')

    #inverse gft
    recon_sig=[]
    for t in range(no_frames):
        temp=recon_sig_idct[t,:,:]

        recon_sig_perframe = np.matmul(v, temp)
        recon_sig.append(recon_sig_perframe)
    recon_sig=np.array(recon_sig)

# computing mean absolute error
    e= abs(recon_sig - data)
    mae = np.mean(e)

    bits = 0
    for i in range(len(encoding_x)):
        bits += len(encoding_x[i])

    for i in range(len(encoding_y)):
        bits += len(encoding_y[i])

    # separate x and y
    recon_sig_x = recon_sig[:, :, 0]
    recon_sig_y = recon_sig[:, :, 1]
    # posex and posey
    return encoding_x, encoding_y, recon_sig, recon_sig_x, recon_sig_y

if __name__=='__main__':
    #define data before you run this independently
    skel_comp(data, no_frames, no_joints, no_coord, device)
    # add arguments for qt matrix
    parser = argparse.ArgumentParser()
    parser.add_argument('--inc', type=int, help='custom increment', default=10)
    parser.add_argument('--sub', type=int, help='custom quantization table', default=50)
    args = parser.parse_args()
    answer = custom_qt(args.inc, args.sub)
