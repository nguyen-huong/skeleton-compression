# real-time camera feed using tensorflow, mediapipe, cv2, and posenet to extract skeleton data, store it in a json file, and then compress it.
#input: live skeleton data
#output: compressed data

import mediapipe as mp
import numpy as np
import cv2
import tensorflow as tf
from posenet import *
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import time
import random

cap = cv2.VideoCapture(0)
#setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
  while cap.isOpened():
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    fps_start = time.time()
    prev_time = 0
    if fps_start > prev_time:
      prev_time += fps_start
      fps_start = time.time()
      fps = 1.0 / (fps_start - prev_time)

# tuple of poses, scores, and keypoints
    restup = pose.process(image)

# draw the pose on the image
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # get keypoints
    try:
      landmarks = restup.pose_landmarks.landmark
      # json dump x,y coordinates
      json_landmarks = []
      #for every 30 frames, get the keypoints
      for landmark in landmarks:
          json_landmarks.append({
                "Posex": landmark.x,
                "Posey": landmark.y
           })

      for i in range(len(json_landmarks)):
          # print every 30 frames
          if i % 30 == 0:
              skel_data = json_landmarks[i:i+30]
              np.array(skel_data)
              # count increases every time print is called
              current_time = time.time()
              # create a new file every 30 seconds
              if current_time > prev_time:
                  mkdir_path = './frames' + '/' + str(current_time)
                  os.mkdir(mkdir_path)
                  # new json file
                  with open(mkdir_path + '/' + str(current_time) + '.json', 'w') as outfile:
                      json.dump(skel_data, outfile)
                      prev_time += current_time

      # angles
      shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
      elbow_left = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
      wrist_left = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
      hand_left = [landmarks[mp_pose.PoseLandmark.LEFT_HAND.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HAND.value].y]
      hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
      knee_left = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
      ankle_left = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
      foot_left = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT.value].y]
      nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
      eye_left = [landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y]
      eye_right = [landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y]
      ear_left = [landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y]
      ear_right = [landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y]
      neck = [landmarks[mp_pose.PoseLandmark.NECK.value].x, landmarks[mp_pose.PoseLandmark.NECK.value].y]
      shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
      elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
      wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
      hand_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HAND.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HAND.value].y]
      hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
      knee_right = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
      ankle_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
      foot_right = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT.value].y]

    # get angles
      pipeline = rs.pipeline()
      config = rs.config()
      config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
      pipeline.start(config)
      # get frames from the camera
      frames = pipeline.wait_for_frames()
      # get depth data
      depth_frame = frames.get_depth_frame()
      depth_image = np.asanyarray(depth_frame.get_data())


#print out error
    except Exception as e:
        cv2.putText(frame, "Error: {}".format(e), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # draw
    mp_drawing.draw_landmarks(image, restup.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

    cv2.imshow('Compression Feed', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  fps.stop()
  cap.release()
  cv2.destroyAllWindows()