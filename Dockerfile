FROM centos
MAINTAINER Hamza EL-HAFYANI
RUN yum -y update
RUN yum -y install yum-utils
RUN yum -y groupinstall development
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install python36u
RUN yum -y install python-pip
RUN pip install  --upgrade pip
RUN pip install  virtualenv

