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


epoch_time_known = 1695935313
epoch_time_bytes = epoch_time_known.to_bytes(4, byteorder='little', signed=False)
epoch_time_offset = binary_data.find(epoch_time_bytes)


epoch_time_offset_bits = epoch_time_offset * 8
bstream.pos = epoch_time_offset_bits


epoch_time = bstream.read('intle:32')


person_id = bstream.read('intle:32')


skeleton_confidence = bstream.read('intle:8')

# explicit padding
bstream.pos += 24


screen_width = bstream.read('uintle:16')
screen_height = bstream.read('uintle:16')


skeleton_x = bstream.read('intle:16')
skeleton_y = bstream.read('intle:16')


event_type = bstream.read('uintle:8')
level = bstream.read('uintle:8')


num_frames = bstream.read('uintle:16')

print({
    'epoch_time': epoch_time,
    'person_id': person_id,
    'skeleton_confidence': skeleton_confidence,
    'screen_width': screen_width,
    'screen_height': screen_height,
    'skeleton_x': skeleton_x,
    'skeleton_y': skeleton_y,
    'event_type': event_type,
    'level': level,
    'num_frames': num_frames
})

def skip_padding(stream, padding_size):
    stream.pos += padding_size * 8

field_lengths = {
    'alert_version_flag': 32,
    'epoch_time': 32,
    'person_id': 32,
    'skeleton_confidence': 8,
    'explicit_padding': 24,  # 3 bytes padding
    'screen_width': 16,
    'screen_height': 16,
    'skeleton_x': 16,
    'skeleton_y': 16,
}


# iterate thru frames
for _ in range(num_frames):
    # Read the frame header
    timestamp_seconds = bstream.read('uintle:16')
    action_label = bstream.read('uintle:8')
    number_of_key_points = bstream.read('uintle:8')
 
skip_padding(bstream, 16)  

number_of_key_points = min(number_of_key_points, 18) 
x_coordinates = [[] for _ in range(18)]
y_coordinates = [[] for _ in range(18)] 

    # keypoint structure
for _ in range(number_of_key_points):
        key_point_index = bstream.read('uintle:8')
        key_point_probability = bstream.read('uintle:8') 
        key_point_x = bstream.read('intle:16')  # signed integer for X coordinate
        key_point_y = bstream.read('intle:16')  # signed integer for Y coordinate
        # process each keypoint data
        print(f"Frame {_}: Keypoint {key_point_index}: X = {key_point_x}, Y = {key_point_y}")

        if 0 <= key_point_index < 18:
            x_coordinates[key_point_index].append(key_point_x)
            y_coordinates[key_point_index].append(key_point_y)

# plotting
for i in range(18):
    plt.figure()
    plt.plot(x_coordinates[i], label='X Coordinate')
    plt.plot(y_coordinates[i], label='Y Coordinate')
    plt.title(f'Joint {i}')
    plt.xlabel('Frame Number')
    plt.ylabel('Coordinate Value')
    plt.legend()
    plt.show()



