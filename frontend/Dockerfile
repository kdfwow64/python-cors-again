FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
ADD front-reqs.txt /opt/front-reqs.txt
#ADD front /opt/front
RUN mkdir /opt/log
RUN touch /opt/log/optima-front.log
RUN pip install virtualenv
RUN virtualenv -p python3.6 /opt/frontenv
RUN /opt/frontenv/bin/pip install -r /opt/front-reqs.txt
#CMD  /opt/frontenv/bin/python /opt/front/manage.py runserver 0.0.0.0:8000
#EXPOSE 8000

