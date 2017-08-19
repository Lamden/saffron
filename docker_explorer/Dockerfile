FROM mhart/alpine-node

MAINTAINER james.a.munsch@protonmail.com

RUN apk update && apk add git \
    && git clone https://github.com/carsenk/explorer \
    && cd explorer \
    && npm install \
    && bower install

EXPOSE 8000
ENTRYPOINT ['npm', 'start']