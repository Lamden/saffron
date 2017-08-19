FROM mhart/alpine-node

MAINTAINER james.a.munsch@protonmail.com

RUN apk-update && apk add git \
    && 
    && git clone https://github.com/ethereum/remix \
    && cd remix \
    && npm install \



EXPOSE 8080
ENTRYPOINT ['npm', 'start']