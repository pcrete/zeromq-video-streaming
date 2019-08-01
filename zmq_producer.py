"""
export SERVER_IP=45.121.60.164
export SERVER_IP=127.0.0.1

export SERVER_IP=45.121.60.164
export SERVER_PORT=5555
export HOST_NAME=register
export VIDEO_SRC=0
python zmq_producer.py 

export VIDEO_SRC=http://192.168.2.34:8080/video?.mjpeg


"""
import os
import time
import cv2

from imagezmq import imagezmq
from imutils.video import WebcamVideoStream

# initialize the ImageSender object with the socket address of the server
sender = imagezmq.ImageSender(
    connect_to="tcp://{}:{}".format(
        os.environ["SERVER_IP"], 
        os.environ['SERVER_PORT']
    )
)
print('Connect the ImageSender object to {}:{}'.format(
    os.environ["SERVER_IP"], 
    os.environ['SERVER_PORT'])
)
print('Host name is {}'.format(os.environ["HOST_NAME"]))
print('Video source is {}'.format(os.environ["VIDEO_SRC"]))

# if video source is digit or string
video = os.environ['VIDEO_SRC']
video = int(video) if str.isdigit(video) else video

# initialize the video stream
video_stream = WebcamVideoStream(src=video)

# 4:3=1280x960, 640x480 / 16:9=1280x720, 640x360
video_stream.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_stream.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
video_stream.stream.set(cv2.CAP_PROP_FPS, 24)

print('\nVideo_stream.stream.get')
print(video_stream.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
print(video_stream.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(video_stream.stream.get(cv2.CAP_PROP_FPS),'\n')

video_stream.start()
# a camera warmup time of 2.0 seconds

frame = video_stream.read()
# crop_y to 360
if frame.shape == (480, 640, 3):
    frame = frame[60:-60, :]
print('Video Size is', frame.shape)
print('Streaming frames to the server...')
while True:
    # read the frame from the camera and send it to the server
    frame = video_stream.read()
    
    # crop_y to 360
    if frame.shape == (480, 640, 3):
        frame = frame[60:-60, :]
        # frame = cv2.resize(frame, (1280, 720))
        
    _, jpg_buffer = cv2.imencode(".jpg", frame)
    sender.send_jpg(os.environ["HOST_NAME"], jpg_buffer)
