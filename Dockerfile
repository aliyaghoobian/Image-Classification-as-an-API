FROM python:3.8-slim-buster
RUN mkdir -p /img_class 
WORKDIR /img_class

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app/ .
COPY model/ .

EXPOSE 8000
# VOLUME [“/app-data”]
CMD ["python3", "app/main.py"]
