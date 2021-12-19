# VERSION 1.10.9
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t airflow .
# SOURCE: https://github.com/puckel/docker-airflow

# A Dockerfile must start with ‘FROM’ instruction.
# ‘FROM’ instruction specifies the ‘Base Image’ from which you are building.

# Since Airflow uses python base image ‘python
FROM python:3.7-slim-buster 

# optional instruction which sets the 'Author' field in the generated images
LABEL maintainer="Puckel_"


# 'ENV' instruction sets the environment variable in a key
# these variables are availible inside the container during the build and runtime
# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
# other environment variable
# Define fr_FR. # or en_US
ENV LANGUAGE fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LC_ALL fr_FR.UTF-8
ENV LC_CTYPE fr_FR.UTF-8
ENV LC_MESSAGES fr_FR.UTF-8

# ARG instruction defines the variables that user can pass to the docker image
# during its build time like what will be he version or home path for the image
# Airflow variables
ARG AIRFLOW_VERSION=2.2.0
ARG AIRFLOW_USER_HOME=/opt/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}


# Disable noisy "Handling signal" log messages:
# ENV GUNICORN_CMD_ARGS --log-level WARNING


# 'RUN' directive is used for installing the primary requirements
# for the image we are building. So as to make it pre-loaded with requisites
# it is going to use e.g., which python packages
# RUN instruction executes the given commands in a new layer on top of the current image 
# and then after performing the current instruction it will commit the results in the image
# and moves to the next instruction. This loop will continue till the last command in chain
RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        AF-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# fr_FR.UTF-8 UTF-8$/fr_FR.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=fr_FR.UTF-8 LC_ALL=fr_FR.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install pytz \
    && echo '## plyvel is a package needed for google provide' \
    && pip install plyvel \ 
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && pip install 'redis==3.2' \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

# entrypoint has some set of configurations which are particular to airflow
COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

RUN chown -R airflow: ${AIRFLOW_USER_HOME}

# 'EXPOSE' is for exposing the ports
# So it informs docker runtime network ports
EXPOSE 8080 5555 8793 5444

# USER sets the user name while running the image
USER airflow
# WORKDIR sets the working directory for any instruction written in dockerfile
# like RUN. If you dont specify this workdir, docker will create a directory by itself
WORKDIR ${AIRFLOW_USER_HOME}
# ENTRYPOINT is the script containing commands that will be executed every time
# the image starts. Here we should specify the file path
ENTRYPOINT ["/entrypoint.sh"]
# 'CMD' specifies the arguments that will be fed to the entrypoint script
# Pay attention that this CMD must be unique in this file
# In case you have 2 then the last one will be feded
CMD ["webserver"]
