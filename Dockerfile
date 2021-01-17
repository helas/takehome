FROM python:3.9.1
ENV PYTHONUNBUFFERED=1
WORKDIR /ws_data
COPY ./ws_data/requirements.txt /ws_data/
RUN pip install -r requirements.txt
COPY ./ws_data/ /ws_data/
