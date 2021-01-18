FROM python:3.9.1 as python-base
ENV PYTHONUNBUFFERED=1

from python-base as client
WORKDIR /client_data
COPY ./requirements.txt /client_data/
RUN pip install -r requirements.txt
COPY . /client_data/
