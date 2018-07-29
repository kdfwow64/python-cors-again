FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
RUN useradd celery
ADD abst-reqs.txt /opt/abst-reqs.txt
#ADD abstraction_layer /opt/abstraction_layer
RUN virtualenv -p python3.6 /opt/notification_env
RUN /opt/notification_env/bin/pip install -r /opt/abst-reqs.txt
RUN touch /opt/optima-notification.log
#CMD cd /opt/abstraction_layer && /opt/abstraction_layer_env/bin/celery -A abstraction_layer worker --loglevel=info -n AbstractionLayer --logfile=/opt/optima-abstraction-layer.log
RUN chown celery -R /opt/