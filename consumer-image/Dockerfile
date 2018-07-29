FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
RUN useradd celery
ADD consumer-reqs.txt /opt/consumer-reqs.txt
RUN virtualenv -p python3.6 /opt/consumer_env
RUN /opt/consumer_env/bin/pip install -r /opt/consumer-reqs.txt
RUN touch /opt/consumer.log
RUN chown celery -R /opt/
