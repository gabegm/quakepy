FROM python:3.11.5-slim-bullseye
LABEL author="Gabriel Gauci Maistre"

RUN apt update && apt install -y gdal-bin libgdal-dev g++

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal

ENV C_INCLUDE_PATH=/usr/include/gdal

ADD . /code
WORKDIR /code

RUN chmod +x install.sh
RUN /bin/bash -c './install.sh'

ENTRYPOINT ["./run.sh"]