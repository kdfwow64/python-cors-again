FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
RUN useradd celery
ADD differ-reqs.txt /opt/differ-reqs.txt
RUN touch /opt/optima-configuration-differ-precheck.log
RUN mkdir /dev/log
RUN mkdir /opt/AutomationTools
RUN mkdir /opt/AutomationTools/cfg
RUN mkdir /opt/AutomationTools/log
RUN touch /opt/AutomationTools/log/configuration_differ_precheck.log
ADD ConfigurationDifferPrecheck.cnf /opt/AutomationTools/cfg/ConfigurationDifferPrecheck.cnf
RUN virtualenv -p python3.6 /opt/configuration-differ-precheck-env
RUN /opt/configuration-differ-precheck-env/bin/pip install -r /opt/differ-reqs.txt
RUN chown celery -R /opt/