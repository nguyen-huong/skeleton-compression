# Project description: 

In conjunction with Altumview Sentinare, we are applying our Graph-based Skeleton Compression (GSC) algorithm from the output coordinates read from Altumview Fall Detection and Activity Sensor Camera. Our existing compression Github can be found in `skeleton_in_Python`. In order to tweak our existing pipeline, we have taken into consideration that the camera recognizes 18 distinct body parts, including feet, knees, hands, and more, effectively creating a stick figure representation of individuals without capturing or transmitting identifiable visual data. By leveraging Altumview camera’s algorithm in face and joint detection, the aim is to effectively extract data coordinates through third-party API, and apply our compression algorithm through a differentiable spatio-temporal graph transform, non-uniform quantization, coefficient scanning, and entropy coding with run-length codes.

# Methodology: 

The project aims to apply the Graph-based Skeleton Compression (GSC) algorithm to efficiently compress and reconstruct skeletal data, embedding it onto Altumview Fall Detection and Activity Sensor Camera for visualization and accuracy assessment, and further utilizing it for action recognition training. Embedding our compressing code allows output of a compacted and efficient value in bits for each coordinate set. The compressed skeletal data will be reconstructed and graphed according to each joint, visualizing the fidelity and variability of the compression algorithm.

# Documentation: 
MQTT API is utilized to extract binary data using the camera's record ID and epoch time.
The binary data is parsed to extract key coordinates for each joint, using C structure definitions as per Altumview’s documentation. Once it is being extracted and parsed, x coordinates should be in a list of “Posex", and y coordinates should be “Posey"
The extracted coordinates are floating-point numbers between 0.0 and 1.0.
Scaled coordinates should be for a canvas size of 960x540 pixels. The scaling maintains a 16:9 aspect ratio, with the X range being 1.77 times larger than the Y range for accuracy.
Each frame has a number of key point structures. Each key point structure contains:
* Key Point Index (8 bits)
* Key Point Probability (fixed 8 bits)
- Key Point X (signed 16 bits): May have negative values.
- Key Point Y (signed 16 bits): Based on (0,0) origin.
Coordinates are reshaped into number of joints and frame, then segment based on number of frames transfer (30)
* Compression (skel_comp) is applied to X and Y arrays separately
* This outputs a pair of arrays (recon_sig_x and recon_sig_y), which hold the reconstructed signals for X and Y coordinates after compression

# Current Progress: 
<img width="814" alt="Screenshot 2024-05-17 at 11 16 11 PM" src="https://github.com/nguyen-huong/skeleton-compression/assets/57471582/6466cc1f-049a-4eaf-9b85-aa338096b896">
<img width="814" alt="Screenshot 2024-05-17 at 11 17 43 PM" src="https://github.com/nguyen-huong/skeleton-compression/assets/57471582/aa6a4ebe-f8e8-42b9-8aed-41ce2e1dc92c">

One issue with the current code to apply compression  is that, on some trials, it reads movements from non-targeted body parts, despite no movement. For example, the hand and arm (Joints 2-7) could be moving while the legs are not moving, but the algorithm results show movement from the leg, marked by some spikes. This may be due to the process of extracting data, in which converted binary data does not match the final format. Another theory is that plotting inside each loop repeats multiple times throughout the frames; the correct method may have been to generate plots from all of the data at one time, and plot once outside the loop.

<img width="814" alt="Screenshot 2024-05-17 at 11 26 18 PM" src="https://github.com/nguyen-huong/skeleton-compression/assets/57471582/af83d075-0bdf-41a2-bb9c-9b87b7cf6941">
<img width="814" alt="Screenshot 2024-05-17 at 11 30 46 PM" src="https://github.com/nguyen-huong/skeleton-compression/assets/57471582/be1d0ba9-b5a1-4e32-9cc4-108acbbfa47a">

In some trials, X and Y coordinates plotted the same movement when it should not have. On one trial, the hand may be moving up and down (y-axis), while another trial shows the hand moving side to side (x-axis); but both results plotted on the graph show the same data. This is inaccurate.

# References: 
Das, Pratyusha, and Antonio Ortega. “Graph-Based Skeleton Data Compression.” 2020 IEEE 22nd International Workshop on Multimedia Signal Processing (MMSP), 21 Sept. 2020, ieeexplore.ieee.org/document/9287103, 10.1109/mmsp48831.2020.9287103.

Kay, W., Carreira, J., Simonyan, K., Zhang, B., Hillier, C., Vijayanarasimhan, S., ... & Zisserman, A. (2017). The kinetics human action video dataset. arXiv preprint arXiv:1705.06950

Agarwal, A. (2022). Methods for Gait Analysis in a Supportive Smart Home. Master's thesis, Faculty of Graduate and Postdoctoral Affairs, Carleton University, Ottawa, Ontario.






