FROM ubuntu
MAINTAINER "ahsan ali"
#Install git
RUN apt-get update        
RUN apt-get install -y git
WORKDIR /root       
RUN git clone https://github.com/ahsan-ali3/DataScience-Projects.git

#Set working directory
CMD /bin/bash
