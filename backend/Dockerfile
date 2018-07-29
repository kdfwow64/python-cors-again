FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
ADD back-reqs.txt /opt/back-reqs.txt
ADD back /opt/back
RUN virtualenv -p python3.6 /opt/backenv
RUN /opt/backenv/bin/pip install -r /opt/back-reqs.txt
CMD /opt/backenv/bin/python /opt/back/app.py
#EXPOSE 5000
