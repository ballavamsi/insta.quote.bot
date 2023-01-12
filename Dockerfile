FROM python:3.10
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 python3-dev python3-tk scrot -y
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . /app
WORKDIR /app
RUN mkdir -p /data
CMD ["python", "main.py"]