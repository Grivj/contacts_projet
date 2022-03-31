FROM nginx

RUN apt-get update
RUN apt-get install -y apache2-utils


RUN htpasswd -cdb /usr/.htpasswd admin MyVm1@Hoolders#2015

COPY ./nginx.conf /etc/nginx/nginx.conf
