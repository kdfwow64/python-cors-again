FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
RUN useradd celery
ADD differ-reqs.txt /opt/differ-reqs.txt
RUN touch /opt/optima-configuration-differ-postcheck.log
RUN mkdir /dev/log
RUN mkdir /opt/AutomationTools
RUN mkdir /opt/AutomationTools/cfg
RUN mkdir /opt/AutomationTools/log
RUN touch /opt/AutomationTools/log/configuration_differ_postcheck.log
ADD ConfigurationDifferPostcheck.cnf /opt/AutomationTools/cfg/ConfigurationDifferPostcheck.cnf
RUN virtualenv -p python3.6 /opt/configuration-differ-postcheck-env
RUN /opt/configuration-differ-postcheck-env/bin/pip install -r /opt/differ-reqs.txt
RUN chown celery -R /opt/