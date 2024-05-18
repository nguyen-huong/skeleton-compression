import requests
import struct
import json
import matplotlib.pyplot as plt

# client and endpoint information
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
if response.status_code == 200:
    json_data = response.json()
    access_token = json_data["access_token"]
else:
    print("Error getting access token:", response.text)

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + access_token,
}

# binary data
endpoint = "https://api.altumview.com/v1.0/recordings/8283/1695935313"
response = requests.get(endpoint, headers=headers)
binary_data = response.content

def prob_value(binary_data, start_offset):
    possible_prob_values = {}
    
    for offset in range(start_offset, len(binary_data) - 1, 4):  # 4 bytes = BinaryAlertKeyPoint
        prob = struct.unpack_from('<B', binary_data, offset + 1)[0]  #skip keyPointIndex
        possible_prob_values[prob] = possible_prob_values.get(prob, 0) + 1
        
    return max(possible_prob_values, key=possible_prob_values.get)

# return keypoints
def find_keypoints(binary_data, fixed_prob, start_offset):
    keypoints = []
    offset = start_offset

    while True:
        pos = binary_data.find(struct.pack('<B', fixed_prob), offset)
        if pos == -1:
            break
        
        keyPointIndex, _, X, Y = struct.unpack_from('<BBhh', binary_data, pos - 1)
        keypoints.append((keyPointIndex, fixed_prob, abs(X), abs(Y)))
        offset = pos + 1

    return keypoints


def unpack(binary_data):
    epoch_offset = binary_data.find(struct.pack('<I', 1695935313))
    version, = struct.unpack_from('<I', binary_data, epoch_offset - 4)
    personID, = struct.unpack_from('<i', binary_data, epoch_offset + 4)
    skeletonConfidence, = struct.unpack_from('<B', binary_data, epoch_offset + 8)
    screenWidth, screenHeight = struct.unpack_from('<HH', binary_data, epoch_offset + 12)
    x, y = struct.unpack_from('<hh', binary_data, epoch_offset + 16)
    event_type, = struct.unpack_from('<B', binary_data, epoch_offset + 20)
    level, = struct.unpack_from('<B', binary_data, epoch_offset + 21)
    numFrames, = struct.unpack_from('<h', binary_data, epoch_offset + 22)

    print("Version:", version)
    print("Epoch Time:", 1695935313)
    print("Person ID:", personID)
    print("Skeleton Confidence:", skeletonConfidence)
    print("Screen Width:", screenWidth)
    print("Screen Height:", screenHeight)
    print("Skeleton X location:", x)
    print("Skeleton Y location:", y)
    print("Event Type:", event_type)
    print("Level:", level)
    print("Number of Frames:", numFrames)
    
    x_values = []
    y_values = []

    frame_offset = epoch_offset + struct.calcsize('<IIiB3BHHhhBBh')
    for _ in range(numFrames):
        msDelta, action, numKeyPoints, x0, y0, x1, y1, *probs = struct.unpack_from('<HBBhhhh8B', binary_data, frame_offset)
        frame_offset += struct.calcsize('<HBBhhhh8B')

        fixed_prob = prob_value(binary_data, frame_offset)

    # keypoints
        all_keypoints = []
        keypoints = find_keypoints(binary_data, fixed_prob, frame_offset)
        for kp in keypoints:
            _, _, x, y = kp
            x_values.append(x)
            y_values.append(y)
            # print(f"Key Point Index: {kp[0]}, Probability: {kp[1]}, X: {kp[2]}, Y: {kp[3]}")

keypoints_dict = unpack(binary_data)
keypoints_x = keypoints_dict['x']
keypoints_y = keypoints_dict['y']
fig, axes = plt.subplots(18, 2, figsize=(10, 90))  

for joint_index in range(18):
    # x coordinates
    axes[joint_index, 0].plot(keypoints_x[joint_index], 'o-')
    axes[joint_index, 0].set_title(f'Joint {joint_index} X Coordinates')
    axes[joint_index, 0].set_xlabel('Frame')
    axes[joint_index, 0].set_ylabel('X coordinate')

    # y coordinates
    axes[joint_index, 1].plot(keypoints_y[joint_index], 'o-')
    axes[joint_index, 1].set_title(f'Joint {joint_index} Y Coordinates')
    axes[joint_index, 1].set_xlabel('Frame')
    axes[joint_index, 1].set_ylabel('Y coordinate')

plt.tight_layout()
plt.show()