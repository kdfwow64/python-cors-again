FROM basic_centos7
MAINTAINER Hamza EL-HAFYANI
RUN useradd celery
ADD differ-reqs.txt /opt/differ-reqs.txt
RUN touch /opt/optima-configuration-image-loader.log
RUN mkdir /dev/log
RUN mkdir /opt/AutomationTools
RUN mkdir /opt/AutomationTools/cfg
RUN mkdir /opt/AutomationTools/log
RUN touch /opt/AutomationTools/log/configuration_image_loader.log
ADD ConfigurationImageLoader.cnf /opt/AutomationTools/cfg/ConfigurationImageLoader.cnf
RUN virtualenv -p python3.6 /opt/configuration-image-loader-env
RUN /opt/configuration-image-loader-env/bin/pip install -r /opt/differ-reqs.txt
RUN chown celery -R /opt/