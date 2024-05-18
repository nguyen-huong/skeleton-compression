import bitstring
import requests
import struct
import numpy as np
import matplotlib.pyplot as plt

import json
client_id = "N4P6DT57vRSAwu0p"
client_secret = "tskOEQhYC8uuYhG1x1D4TWF41SdaX2Lw5ohbfP3SAHJBmI43uEb9Uk1lDf4aiqtk"
authorization_endpoint = "https://oauth.altumview.com/v1.0/authorize"
token_endpoint = "https://oauth.altumview.com/v1.0/token"
permission = "camera:write, camera:read"

# access token
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': permission,
}
response = requests.post(token_endpoint, data=data)
response.raise_for_status() 
json_data = response.json()
access_token = json_data["access_token"]

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + access_token,
}


# binary data
endpoint = "https://api.altumview.com/v1.0/recordings/8283/1695935313"
response = requests.get(endpoint, headers=headers)
response.raise_for_status()
binary_data = response.content

bstream = bitstring.BitStream(binary_data)


# get the fixed probability value
def skip_padding(stream, padding_size):
    stream.pos += padding_size * 8


alert_version_flag = bstream.read('uint:32')
epoch_time = bstream.read('intle:32')
person_id = bstream.read('int:32')
skeleton_confidence = bstream.read('uint:8')
skip_padding(bstream, 3)
screen_width = bstream.read('uint:16')
screen_height = bstream.read('uint:16')
skeleton_x = bstream.read('int:16')
skeleton_y = bstream.read('int:16')
event_type = bstream.read('uint:8')
level = bstream.read('uint:8')
number_of_frames = bstream.read('uint:16')

x_positions = []
y_positions = []
scaled_x_positions = []
scaled_y_positions = []

# get the keypoint data
for frame_number in range(number_of_frames):

    timestamp_seconds = bstream.read('uint:16')
    action_label = bstream.read('uint:8')
    number_of_key_points = bstream.read('uint:8')
    human_bounding_box = bstream.read('bytes:8') 
    action_label_probabilities = bstream.read('bytes:7') 
    skip_padding(bstream, 1)  

  
    keypoints = []
    for keypoint_index in range(number_of_key_points):
        kp_index = bstream.read('uint:8')
        kp_probability = bstream.read('uint:8')  
        kp_x = bstream.read('int:16')
        kp_y = bstream.read('int:16')

        if kp_index == 7:
            x_positions.append(kp_x)
            scaled_x_positions.append((kp_x//65534)) # divide by screen width
            y_positions.append(kp_y)
            scaled_y_positions.append((kp_y//65535)) # divide by screen height
        keypoints.append({
            'kp_index': kp_index,
            'kp_probability': kp_probability,
            'kp_x': kp_x,
            'kp_y': kp_y
        })


        print(f"Frame {frame_number}: Keypoint {kp_index}: X = {kp_x}, Y = {kp_y}")


    plt.figure(figsize=(14, 6))


    plt.subplot(1, 2, 1)  
    plt.plot(x_positions, 'b-', label='X Positions')
    plt.xlabel('Frame')
    plt.ylabel('X Position')
    plt.title('X Positions for Keypoint Index 7')
    plt.legend()


    plt.subplot(1, 2, 2)  
    plt.plot(y_positions, 'r-', label='Y Positions')
    plt.xlabel('Frame')
    plt.ylabel('Y Position')
    plt.title('Y Positions for Keypoint Index 7')
    plt.legend()

plt.tight_layout()
plt.show()

