# ZeroMQ Video Streaming

**ZeroMQ** is a high-performance asynchronous messaging library, aimed at use in distributed or concurrent applications. It provides a message queue, but unlike message-oriented middleware, a ZeroMQ system can run without a dedicated message broker. The library's API is designed to resemble Berkeley sockets.

**PyZMQ** provides python bindings for ØMQ and allows you to leverage ØMQ in python applications. I have been using pyzmq-static with virtualenv as it neatly provides isolated sandbox for my learning.

**ImageZMQ** is a set of Python classes that transport OpenCV images from one computer to another using PyZMQ messaging. For example, here is a screen on a Mac computer showing simultaneous video streams from 8 Raspberry Pi cameras.

## Build Image

```bash
docker build -t zmq_consumer .
docker tag zmq_consumer pcrete/zmq_consumer
docker push pcrete/zmq_consumer
```

## Run Consumer

```bash
# example commands
docker run -d --network=host pcrete/zmq_consumer
# or
docker run --rm -it \
--network=host \
-e SERVER_PORT=5555 \
pcrete/zmq_consumer
```

### Console Output

```bash
Open Port is tcp://*:5555
Receiving frames...
Producer connected >> register: 360 640 3
```

## Run Producer

```bash
# example commands
docker run --rm -it \
--network=host \
--device=/dev/video0 \
-e SERVER_IP=127.0.0.1 \
-e SERVER_PORT=5555 \
-e HOST_NAME=evaluator \
-e VIDEO_SRC=0 \
pcrete/zmq_producer
```

### Console Output

```bash
Connect the ImageSender object to 127.0.0.1:5555
Host name is register
Streaming frames to the server...
```
