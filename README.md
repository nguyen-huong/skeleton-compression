# Introduction
This repository holds the codebase for real-time skeleton data compression. We use the methodology proposed in the following paper.


Das, Pratyusha, and Antonio Ortega. “Graph-Based Skeleton Data Compression [1]


# Graph Based-Sketon‌ Compression
Graph-based Skeleton Compression (GSC) is an efficient graph-based method for nearly lossless compression. 

We use a separable spatio-temporal graph transform along with non-uniform quantization, coefficient scanning and entropy coding with run-length codes for nearly lossless compression. We take in output skeletal key points that are associated with (x, y) coordinates in real time. Attached is our pipeline below

<img width="562" alt="Screen Shot 2022-10-28 at 5 16 37 PM" src="https://user-images.githubusercontent.com/57471582/198752937-f5373596-fca7-4f39-918d-093f2110e3c0.png">

We are utilizing the MoveNet TensorFlowLite model to extract skeletal data points and run it through our algorithm. The compression code is embedded within this file, once run, will output
Compressed value in bits for each x and y coordinate sets.

<img width="562" alt="Screen Shot 2022-10-28 at 5 19 17 PM" src="https://user-images.githubusercontent.com/57471582/198753044-1bfcb4c5-5265-4a19-9806-6a8b23274c34.png">

# Visualization of Skeletal Detection

## Visualization of the reconstructed signal from the compressed motion capture data
This is the test for one video data from the action file of cartwheeling. The reconstruction signal of the compressed motion capture data is graphed and drew on to the video data to visualize the accuracy of our compression algorithm. The video data file can be found here: ​​https://drive.google.com/file/d/1EN_kW4dV4_1AfuweUttFjD2V1CKuZtcl/view?usp=sharing

![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/57471582/198753163-f960eb15-e9f6-4cc8-aeb3-e1520fc4325b.gif)

## Real-time compression of the motion capture data

https://user-images.githubusercontent.com/57471582/198753246-aa14e805-2705-471d-9f59-bb7324776ecb.mov



