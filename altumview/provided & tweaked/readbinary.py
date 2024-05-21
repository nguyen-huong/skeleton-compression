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

# parameters to get access token based on OAuth 2.0
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': permission,
}
# send request to get access token
response = requests.post(token_endpoint, data=data)
response.raise_for_status() 
json_data = response.json()
access_token = json_data["access_token"]

# parameters to get binary data
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + access_token,
}

# get binary data using camera ID (8283) and epoch time (1695935313)
endpoint = "https://api.altumview.com/v1.0/recordings/8283/1695935313"
response = requests.get(endpoint, headers=headers)
response.raise_for_status()
# binary data returned from the API
binary_data = response.content
# convert binary data to bitstream
bstream = bitstring.BitStream(binary_data)

# get the position of epoch time in the binary data
epoch_time_known = 1695935313
epoch_time_bytes = epoch_time_known.to_bytes(4, byteorder='little', signed=False)
epoch_time_offset = binary_data.find(epoch_time_bytes)

# set the position of bitstream to the position of epoch time
epoch_time_offset_bits = epoch_time_offset * 8
bstream.pos = epoch_time_offset_bits

# read the epoch time
epoch_time = bstream.read('intle:32')

# read the person ID
person_id = bstream.read('intle:32')

# read the skeleton confidence
skeleton_confidence = bstream.read('intle:8')

# Skip Explicit Padding
bstream.pos += 24


# screen_width = bstream.read('uintle:16')
# screen_height = bstream.read('uintle:16')


# get the position of skeleton x and y to extract the skeleton x and y key points
skeleton_x = bstream.read('intle:16')
skeleton_y = bstream.read('intle:16')

# read the event type and level
event_type = bstream.read('uintle:8')
level = bstream.read('uintle:8')

# read the number of frames
num_frames = bstream.read('uintle:16')

print({
    'epoch_time': epoch_time,
    'person_id': person_id,
    'skeleton_confidence': skeleton_confidence,
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
# print the value of each field

for field_name, field_length in field_lengths.items():
    field_value = bstream.read(f'uintle:{field_length}')
    print(f'{field_name}: {field_value}')
