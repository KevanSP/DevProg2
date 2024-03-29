# A dockerfile must always start by importing the base image.
# We use the keyword 'FROM' to do that.
# In our example, we want import the python image.
# So we write 'python' for the image name and 'latest' for the version.
FROM python:3.9

# In order to launch our python code, we must import it into our image.
# We use the keyword 'COPY' to do that.
# The first parameter 'Sensors.py' is the name of the file on the host.
# The second parameter '/' is the path where to put the file on the image.
# Here we put the file at the image root folder.
RUN apt update
RUN apt upgrade -y
RUN apt-get install -y libopenblas-base cmake
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt install -y python3-picamera2
COPY hal ./hal
COPY Sensors.py .
COPY main.py .
COPY Notification.py .
COPY labels.txt .
COPY model_unquant.tflite .


# We need to define the command to launch when we are going to run the image.
# We use the keyword 'CMD' to do that.
# The following command will execute "python ./Sensors.py".

CMD [ "python3", "./main.py" ]