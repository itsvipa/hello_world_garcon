FROM centos:centos7

WORKDIR /var/app

# Update and install common packages
RUN yum -y update
RUN yum -y install which epel-release java-1.8.0-openjdk java-1.8.0-openjdk-devel curl git tar zip openssl openssl-devel glibc-common

# Install python 3.6
RUN yum -y install gcc python36 python36-libs python36-devel python36-pip

ADD . /var/app

# Install pipenv
RUN        ln -s /usr/bin/pip3.6 /usr/bin/pip
RUN        /usr/bin/pip install pipenv

# Explicitly set locale and related env vars to use en_US.UTF-8
RUN        localedef -c -f UTF-8 -i en_US en_US.UTF-8
ENV        LC_ALL=en_US.UTF-8
ENV        LANG=en_US.UTF-8
# Prevent irrelevant warnings from cluttering Kibana
ENV PYTHONWARNINGS="ignore::UserWarning:cffi.cparser.py"

# Install requirements
RUN        if [ -f /var/app/Pipfile.lock ]; then pipenv install --ignore-pipfile --system; fi

# Add tmp workspace
RUN mkdir /tmp/feed_workspace
RUN chmod 755 /tmp/feed_workspace

ENTRYPOINT ["pipenv", "run"]
