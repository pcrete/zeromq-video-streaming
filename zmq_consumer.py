# python zmq_consumer.py --port 5555

import os
import cv2
import redis
import argparse
import numpy as np
import imagezmq

try:
    server_port = os.environ['SERVER_PORT']
except Exception as ex:
    server_port = '5555'

open_port = 'tcp://*:{}'.format(server_port)
image_hub = imagezmq.ImageHub(open_port=open_port)

print('Open Port is {}'.format(open_port))

r = redis.Redis(host='localhost', port=6379, db=0)

print('Receiving frames...')

hosts = {}
# show streamed images
while True:
    try:
        # tpye(jpg_buffer) is <class 'zmq.sugar.frame.Frame'>
        host_name, jpg_buffer = image_hub.recv_jpg()
        
        # image is 1-d numpy.ndarray and decode to 3-d array
        image = np.frombuffer(jpg_buffer, dtype='uint8')
        image = cv2.imdecode(image, -1)
        
        width, height, channel = image.shape
                
        if host_name not in hosts:
            hosts[host_name] = True
            print('Producer connected >>', host_name+':', width, height, channel)
        
        # image.tostring is <class 'bytes'>
        r.set(host_name, image.tostring())
        r.set(host_name+'_width', width)
        r.set(host_name+'_height', height)
        r.set(host_name+'_channel', channel)
        
        # cv2.imshow(host_name, image)
        # cv2.waitKey(1)
        image_hub.send_reply(b'OK')
        
    except Exception as ex:
        print(ex)
