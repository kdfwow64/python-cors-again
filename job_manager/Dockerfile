FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
RUN useradd celery
ADD orch-reqs.txt /opt/orch-reqs.txt
RUN virtualenv -p python3.6 /opt/job_manager_env
RUN /opt/job_manager_env/bin/pip install -r /opt/orch-reqs.txt
RUN touch /opt/optima-job-manager.log
#CMD cd /opt/abstraction_layer && /opt/abstraction_layer_env/bin/celery -A abstraction_layer worker --loglevel=info -n AbstractionLayer --logfile=/opt/optima-abstraction-layer.log
RUN chown celery -R /opt/