FROM python:3.9.1 as python-base
ENV PYTHONUNBUFFERED=1

FROM python-base as web-service
WORKDIR /ws_data
COPY ./ws_data/requirements.txt /ws_data/
RUN pip install -r requirements.txt
COPY ./ws_data/ /ws_data/
#
# from python-base as client
# WORKDIR /client_data
# COPY ./client_data/requirements.txt /client_data/
# RUN pip install -r requirements.txt
# COPY ./client_data/ /client_data/
#
# from python-base as loader
# WORKDIR /etl_data
# COPY ./etl_data/requirements.txt /etl_data/
# RUN pip install -r requirements.txt
# COPY ./etl_data/ /etl_data/