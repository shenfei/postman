FROM ubuntu:18.04
ENV LANG=C.UTF-8
ARG APT_INSTALL="apt-get install -y --no-install-recommends"
ARG PIP_INSTALL="python -m pip --no-cache-dir install"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive ${APT_INSTALL} pandoc
RUN DEBIAN_FRONTEND=noninteractive ${APT_INSTALL} \
        python3 \
        python3-dev \
        python3-pip
RUN ln -s /usr/bin/python3 /usr/local/bin/python3 && \
    ln -s /usr/bin/python3 /usr/local/bin/python

RUN ${PIP_INSTALL} pip --upgrade
RUN ${PIP_INSTALL} setuptools && \
        ${PIP_INSTALL} requests PyYAML
