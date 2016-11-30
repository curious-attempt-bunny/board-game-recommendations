# Based on https://hub.docker.com/r/p0bailey/docker-flask/~/dockerfile/

FROM ubuntu:14.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y python-pip python-dev

RUN pip install numpy 
RUN pip install pandas
RUN pip install flask

RUN mkdir -p /var/src/app/templates

WORKDIR /usr/src/app
ADD metadata.csv metadata.csv
ADD similarity.csv similarity.csv
ADD server.py server.py
ADD templates templates

EXPOSE 5000
CMD ["python", "server.py"]
