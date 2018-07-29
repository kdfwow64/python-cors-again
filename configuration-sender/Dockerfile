FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
RUN useradd celery
ADD agent-reqs.txt /opt/agent-reqs.txt
RUN touch /opt/optima-configuration-sender.log
RUN mkdir /dev/log
RUN mkdir /opt/AutomationTools
RUN mkdir /opt/AutomationTools/cfg
RUN mkdir /opt/AutomationTools/log
RUN touch /opt/AutomationTools/log/configuration_sender.log
ADD ConfigurationSender.cnf /opt/AutomationTools/cfg/ConfigurationSender.cnf
RUN virtualenv -p python3.6 /opt/configuration-sender-env
RUN /opt/configuration-sender-env/bin/pip install -r /opt/agent-reqs.txt
RUN chown celery -R /opt/
