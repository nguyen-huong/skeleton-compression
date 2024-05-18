import struct

BINARY_ALERT_HEADER_FORMAT = '<IIiB3HhHhBBh'

def print_bytes(data, offset, length=16):
    slice = data[offset:offset + length]
    hex_values = ' '.join([f"{b:02x}" for b in slice])
    print(f"offset {offset}: {hex_values}")

def read_uint32(data, offset):
    if len(data) - offset < 4:
        return None, offset
    value, = struct.unpack_from('<I', data, offset)
    offset += 4
    return value, offset

def read_int32(data, offset):
    if len(data) - offset < 4:
        return None, offset
    value, = struct.unpack_from('<i', data, offset)
    offset += 4
    return value, offset

def read_uint16(data, offset):
    if len(data) - offset < 2:
        return None, offset
    value, = struct.unpack_from('<H', data, offset)
    offset += 2
    return value, offset

def read_int16(data, offset):
    if len(data) - offset < 2:
        return None, offset
    value, = struct.unpack_from('<h', data, offset)
    offset += 2
    return value, offset

def read_uint8(data, offset):
    if len(data) - offset < 1:
        return None, offset
    value, = struct.unpack_from('<B', data, offset)
    offset += 1
    return value, offset

def read_probs(data, offset):
    if len(data) - offset < 7:
        return None, offset
    probs_data = struct.unpack_from('7B', data, offset)
    probs = list(probs_data)
    offset += 7
    return probs, offset

def unpack_alert(data, offset):
    version, offset = read_uint32(data, offset)
    if version is None:
        return None, offset
    
    when, offset = read_uint32(data, offset)
    personID, offset = read_int32(data, offset)
    skeletonConfidence, offset = read_uint8(data, offset)

    # Padding
    offset += 3

    screenWidth, offset = read_uint16(data, offset)
    screenHeight, offset = read_uint16(data, offset)
    x, offset = read_int16(data, offset)
    y, offset = read_int16(data, offset)
    eventType, offset = read_uint8(data, offset)
    level, offset = read_uint8(data, offset)
    numFrames, offset = read_int16(data, offset)

    frames = []
    for _ in range(numFrames):
        if len(data) - offset < struct.calcsize('HBB'):
            break

        msDelta, offset = read_uint16(data, offset)
        action, offset = read_uint8(data, offset)
        numKeyPoints, offset = read_uint8(data, offset)

        if len(data) - offset < struct.calcsize('hhhh7B'):
            break

        x0, offset = read_int16(data, offset)
        y0, offset = read_int16(data, offset)
        x1, offset = read_int16(data, offset)
        y1, offset = read_int16(data, offset)

        probs, offset = read_probs(data, offset)
        if probs is None:
            break

        key_points = []
        for _ in range(numKeyPoints):
            if len(data) - offset < struct.calcsize('BBhh'):
                break
            
            keyPointIndex, offset = read_uint8(data, offset)
            keyPointProb, offset = read_uint8(data, offset)
            X, offset = read_int16(data, offset)
            Y, offset = read_int16(data, offset)
            
            key_points.append((keyPointIndex, keyPointProb, X, Y))

        frame = {
            "msDelta": msDelta,
            "action": action,
            "numKeyPoints": numKeyPoints,
            "bbox": (x0, y0, x1, y1),
            "action_probs": probs,
            "key_points": key_points
        }

        frames.append(frame)

    alert = {
        "version": version,
        "when": when,
        "personID": personID,
        "skeletonConfidence": skeletonConfidence,
        "screenWidth": screenWidth,
        "screenHeight": screenHeight,
        "x": x,
        "y": y,
        "eventType": eventType,
        "level": level,
        "numFrames": len(frames),
        "frames": frames
    }

    return alert, offset

def unpack_alerts(filename):
    with open(filename, 'rb') as f:
        data = f.read()

    offset = 0
    alerts = []
    while offset < len(data):
        alert, new_offset = unpack_alert(data, offset)
        if alert is not None:
            alerts.append(alert)
        offset = new_offset

    return alerts


filename = 'combined_data.dat'
all_alerts = unpack_alerts(filename)

for idx, alert in enumerate(all_alerts):
    print(f"Alert {idx + 1}: Version={alert['version']}, Timestamp={alert['when']}, PersonID={alert['personID']}")
