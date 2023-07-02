FROM python:3.8-slim-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY exporter.py /app/exporter.py

RUN pip3 install -r requirements.txt

EXPOSE 9877

CMD ["python3" , "/app/exporter.py"]