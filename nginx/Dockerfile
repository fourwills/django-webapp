FROM ubuntu:16.04
MAINTAINER Will Liu "william.q.liu@gmail.com"
RUN apt-get update -y
RUN apt-get install -y build-essential nginx curl vim 
WORKDIR /etc/nginx
RUN rm -v /etc/nginx/sites-available/default
RUN rm -v /etc/nginx/sites-enabled/default
ADD confs/sites/beats /etc/nginx/sites-enabled/beats
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]