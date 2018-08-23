FROM ubuntu:16.04

RUN apt-get update && apt-get install -yq --no-install-recommends \
     locales \
     vim \
     curl wget \
     python-setuptools python-pip python-dev build-essential \
     git \
     && apt-get clean && \
     rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen \
    && mkdir /guesscat

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt 

ADD server.py starter.py  /guesscat/
COPY tests  /guesscat/tests
COPY static  /guesscat/static
COPY templates  /guesscat/templates