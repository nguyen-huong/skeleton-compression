# Introduction
This repository holds the codebase for real-time skeleton data compression. We use the methodology proposed in the following paper.


Das, Pratyusha, and Antonio Ortega. “Graph-Based Skeleton Data Compression [1]


# Graph Based-Sketon‌ Compression
Graph-based Skeleton Compression (GSC) is an efficient graph-based method for nearly lossless compression. 

We use a separable spatio-temporal graph transform along with non-uniform quantization, coefficient scanning and entropy coding with run-length codes for nearly lossless compression. We take in output skeletal key points that are associated with (x, y) coordinates in real time. Attached is our pipeline below

<img width="839" alt="Screenshot 2022-11-18 at 2 50 32 PM" src="https://user-images.githubusercontent.com/57471582/202817419-20081f37-b8eb-4f05-9cb9-d588839f61e2.png">


We are utilizing the MoveNet TensorFlowLite model to extract skeletal data points and run it through our algorithm. The compression code is embedded within this file, once run, will output
Compressed value in bits for each x and y coordinate sets.

<img width="875" alt="Screenshot 2022-11-18 at 2 50 18 PM" src="https://user-images.githubusercontent.com/57471582/202817437-97e21db8-a1fb-493c-81a8-09560e8c8070.png">


# Visualization of Skeletal Detection

## Visualization of the reconstructed signal from the compressed motion capture data
This is the test for one video data from the action file of cartwheeling. The reconstruction signal of the compressed motion capture data is graphed and drew on to the video data to visualize the accuracy of our compression algorithm. The video data file can be found here: ​​https://drive.google.com/file/d/1EN_kW4dV4_1AfuweUttFjD2V1CKuZtcl/view?usp=sharing



https://user-images.githubusercontent.com/57471582/202965726-a05d6200-3d39-4616-a2b6-e08335592264.mov








## Real-time compression of the motion capture data

https://user-images.githubusercontent.com/57471582/198753246-aa14e805-2705-471d-9f59-bb7324776ecb.mov

# Prerequisites
Python3 (>3.5)

TensorFlow Lite

Other Python libraries can be installed by pip install -r requirements.txt

# Installation
```
git clone --recursive https://github.com/nguyen-huong/skel-compression.git

cd skeleton-in-python/
pip install -r requirements.txt

cd skeleton_in_python
```

# Demo
```
python posenet.py –path ${PATH_TO_VIDEO} -store ${PATH_TO_STORAGE}
```

By default,  we are using our proposed nonlinear quantization matrix as defined in the file quantizationmatrix.txt. We have already experimented with the choice of parameters, and heuristic parameters value are given in quantizationmatrix.txt and error of significance of 2 pixels per join.  However, if you want to use it you can define it here. 

```
python posenet.py –inc${CUSTOMIZE INCREMENT QUANTITY} –sub${CUSTOMIZE INITIAL INCREMENT VALUE}
```

# Activity Recognition using the Compressed File

## Data Preparation
We experimented on two skeleton-based action recognition datasets: Kinetics-skeleton[2].

### Kinetics dataset: 
Kinetics is a dataset for action recognition that only provides raw video clips without skeleton data. First, we extracted skeletons from each frame in Kinetics by using MoveNet. We then run the json files of extracted skeletal data coordinates to our algorithms to output the reconstructed signal as the final compressed version. Our skeletal data is in 2D. 

# Results
The result of bits before and after compression tested on Kinetics datasets are shown as below. Compressed data is reduced to approximately 86% while maintaining video quality compared to state-of-art algorithms. The result of the 50 sampled data can be found in the folder of “test_data” under the name of “compression_error.xlsx".

Link to Kinetics 400 dataset  data points: https://drive.google.com/drive/folders/1Z-XIzo95Cgr73IgALPRGPMlvbkN4HSVo?usp=sharing

Our data have noises in cm and our measures are nearly lossless. The number of bits before are reflected in blue, with a different scale as shown in left axis. The number of bits after are reflected in orange with a different scale as shown in right axis. 

![bits](https://user-images.githubusercontent.com/57471582/205147042-a693f4c8-9469-42c2-bd76-2024c34d3671.jpg)


The graph illustrates the data size or file size once Posenet has saved the file in a stored location for the before results, and once reconstructed, the file size of the saved file after being stored. The yellow line represents the data size before compression, and the red line represents the data size after compression

change to file size before published

![datasize](https://user-images.githubusercontent.com/57471582/205404358-aebea536-83d6-4917-b1b2-f7a77a1ee0cc.jpg)



## Activity recognition performance: 
We selected the following action classes provided—bowling, pullups, bench pressing, parkour, and cartwheeling for activity recognition performance from the Deepmind 400 Kinetics dataset[2] and resulted in an accuracy of 100% before and after if we use the original and the compressed signal. We have extracted on average 300 data points for each action, where 70% of the data is for training and 30% of the data is for testing.

# Contacts
Pratyusha Das
daspraty@usc.edu

Huong Nguyen
huongmng@usc.edu

Antonio Ortega
aortega@usc.edu

# References: 
[1] Das, Pratyusha, and Antonio Ortega. “Graph-Based Skeleton Data Compression.” 2020 IEEE 22nd International Workshop on Multimedia Signal Processing (MMSP), 21 Sept. 2020, ieeexplore.ieee.org/document/9287103, 10.1109/mmsp48831.2020.9287103. 

[2] Kay, W., Carreira, J., Simonyan, K., Zhang, B., Hillier, C., Vijayanarasimhan, S., ... & Zisserman, A. (2017). The kinetics human action video dataset. arXiv preprint arXiv:1705.06950

