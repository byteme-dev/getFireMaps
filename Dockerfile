FROM python:3.8.10-slim

RUN apt update && apt install gcc gdal-bin libgdal-dev g++ -y

WORKDIR /src

COPY . .

RUN pip install -r requirements.txt

CMD python3 index.py