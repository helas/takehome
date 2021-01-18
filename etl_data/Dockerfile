FROM python:3.9.1 as python-base
ENV PYTHONUNBUFFERED=1

from python-base as loader
WORKDIR /etl_data
COPY ./requirements.txt /etl_data/
RUN pip install -r requirements.txt
COPY . /etl_data/