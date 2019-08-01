# Python Image
FROM jjanzic/docker-python3-opencv:opencv-4.0.1

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Configure a container that will run as an executable.
ENTRYPOINT ["python"]

# Execute app.py when the container launches
CMD ["zmq_producer.py"]