# Proof-of-concept
import cv2
import sys
from constants import *
from emotion_recognition import EmotionRecognition
import numpy as np
import urllib
import json
import io
#import to_unicode
cascade_classifier = cv2.CascadeClassifier(CASC_PATH)

def brighten(data,b):
     datab = data * b
     return datab    

def format_image(image):
  if len(image.shape) > 2 and image.shape[2] == 3:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  else:
    image = cv2.imdecode(image, cv2.CV_LOAD_IMAGE_GRAYSCALE)
  faces = cascade_classifier.detectMultiScale(
      image,
      scaleFactor = 1.3,
      minNeighbors = 5
  )
  # None is we don't found an image
  if not len(faces) > 0:
    return None
  max_area_face = faces[0]
  for face in faces:
    if face[2] * face[3] > max_area_face[2] * max_area_face[3]:
      max_area_face = face
  # Chop image to face
  face = max_area_face
  image = image[face[1]:(face[1] + face[2]), face[0]:(face[0] + face[3])]
  # Resize image to network size
  try:
    image = cv2.resize(image, (SIZE_FACE, SIZE_FACE), interpolation = cv2.INTER_CUBIC) / 255.
  except Exception:
    print("[+] Problem during resize")
    return None
  # cv2.imshow("Lol", image)
  # cv2.waitKey(0) image
  #print type(image)
  return image

# Load Model
network = EmotionRecognition()
network.build_network()

def url_to_image(url):
  # download the image, convert it to a NumPy array, and then read
  # it into OpenCV format
  resp = urllib.urlopen(url)
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  return image

num= input("wanna take image(1) or webcam(2)")

if(num==1):
  img = url_to_image("http://www.mobilealabamadentist.com/sites/default/files/BoywithToothBrush.jpg")
  video_capture = img
  frame = video_capture
  result = network.predict(format_image(video_capture))
  result[0][3] = result[0][3] + 0.2
  print type(result)
  feelings_faces = []
  for index, emotion in enumerate(EMOTIONS):
    feelings_faces.append(cv2.imread('./emojis/' + emotion + '.png', -1))
  print "result is"
  print result

elif(num==2):
  #cv2.namedWindow("preview")
  #video_capture = cv2.VideoCapture(0)
  #feelings_faces = []
  #for index, emotion in enumerate(EMOTIONS):
   # feelings_faces.append(cv2.imread('./emojis/' + emotion + '.png', -1))
  #while True:
   ## if video_capture.isOpened():  # try to get the first frame
     # ret, frame = video_capture.read()
    #ret, frame = video_capture.read()
    #cv2.imshow('preview', frame)
    #result = network.predict(format_image(frame))
  video_capture = cv2.VideoCapture(0)

  font = cv2.FONT_HERSHEY_SIMPLEX

  feelings_faces = []
  for index, emotion in enumerate(EMOTIONS):
    feelings_faces.append(cv2.imread('./emojis/' + emotion + '.png', -1))

  while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Predict result with network
    result = network.predict(format_image(frame))

    print "result is"
    print result




#video_capture = cv2.imread('happy.jpg',1)
#print video_capture
#font = cv2.FONT_HERSHEY_SIMPLEX



#while True:
  # Capture frame-by-frame
#ret, frame = video_capture.read()

#print "frame"
#print frame

# Predict result with network
#result = network.predict(format_image(video_capture))

# Draw face in frame
# for (x,y,w,h) in faces:
#   cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

# Write results in frame
if result is not None:
  for index, emotion in enumerate(EMOTIONS):
    cv2.putText(frame, emotion, (10, index * 20 + 20), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 1);
    cv2.rectangle(frame, (130, index * 20 + 10), (130 + int(result[0][index] * 100), (index + 1) * 20 + 4), (255, 0, 0), -1)

  face_image = feelings_faces[result[0].index(max(result[0]))]

  # Ugly transparent fix
  try:
    for c in range(0, 3):
      frame[200:320, 10:130, c] = face_image[:,:,c] * (face_image[:, :, 3] / 255.0) +  frame[200:320, 10:130, c] * (1.0 - face_image[:, :, 3] / 255.0)
  except ValueError:
      print("  ")

# Display the resulting frame
#cv2.imshow('preview', frame)
#if(num==2):
    #if cv2.waitKey(1) & 0xFF == ord('q'):
     # break

# When everything is done, release the capture
if(num==2):
  video_capture.release()
cv2.destroyAllWindows()