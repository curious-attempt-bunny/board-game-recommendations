# Based on https://hub.docker.com/r/p0bailey/docker-flask/~/dockerfile/

FROM ubuntu:14.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y python-pip python-dev

pip install pandas numpy requests

COPY app /var/www/app

EXPOSE 5000
CMD ["python server.py"]