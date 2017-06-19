FROM ubuntu:16.04
MAINTAINER Will Liu "william.q.liu@gmail.com"
RUN apt-get update -y
RUN apt-get install -y build-essential python3-pip python3-dev python3-venv curl vim
COPY ./requirements.txt /web/requirements.txt
WORKDIR /web
RUN pip3 install -r requirements.txt
RUN mkdir -p /var/bp/uploads
COPY . /web
RUN python3 /web/manage.py collectstatic --noinput
EXPOSE 8000