FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
RUN useradd celery
ADD agent-reqs.txt /opt/agent-reqs.txt
RUN touch /opt/agent.log
RUN mkdir /dev/log
RUN mkdir /opt/AutomationTools
RUN mkdir /opt/AutomationTools/cfg
RUN mkdir /opt/AutomationTools/log
RUN touch /opt/AutomationTools/log/agent.log
ADD agent.cnf /opt/AutomationTools/cfg/agent.cnf
RUN virtualenv -p python3.6 /opt/agent-env
RUN /opt/agent-env/bin/pip install -r /opt/agent-reqs.txt
RUN chown celery -R /opt/
